"""
    Vector embeddings classes
"""
import os
import json
# import pandas as pd
import numpy as np
# from io import StringIO

# from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# from google.cloud import aiplatform
# from google.cloud import storage

from vertexai.preview.language_models import TextEmbeddingModel
# import csv

# from vertexai.language_models import CodeGenerationModel
# import pickle
import faiss
from faiss import write_index, read_index

# from tqdm import tqdm
# from sentence_transformers import SentenceTransformer

# import pandas as pd
from pandas import DataFrame

from google.cloud.sql.connector import Connector, IPTypes
import pg8000

import sqlalchemy

ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC



class Nl2Sql_embed():
    """
        Class to work with embeddings using a local file
    """

    def __init__(self):
        """
            Class initialisation function
        """
        self.EMBEDDING_FILE = "../dataset/embeddings.json"
        self.INDEX_FILE = '../vectordb_index/saved_index_localdata'
        self.embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")


    def generate_embedding(self, query, sql='blank sql'):
        """
            Generate embeddings
        """
        # Replace this with your actual embedding generation using text-gecko003 or another model
        q_embeddings = self.embedding_model.get_embeddings([query])[0].values
        sql_embeddings = self.embedding_model.get_embeddings([sql])[0].values

        return q_embeddings, sql_embeddings


    def insert_data(self, question, sql):
        """
            Insert data into the local file
        """
        try:
            with open(self.EMBEDDING_FILE, "r", encoding="utf-8") as inpfile:
                data = json.load(inpfile)
        except FileNotFoundError:
            data = []

        q_emb, sql_emb = self.generate_embedding(question, sql)
        # print(ret_vec)
        data.append({
            "question": question,
            "sql": sql,
            "question_embedding": q_emb,
            "sql_embedding": sql_emb
        })

        with open(self.EMBEDDING_FILE, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile)


    def load_embeddings(self):
        """
            Load embeddings file
        """
        with open(self.EMBEDDING_FILE, "r", encoding="utf-8") as inputfile:
            data = json.load(inputfile)
        return data

    def distance(self, embedding1, embedding2):
        """Calculates negative cosine similarity""" 
        return -cosine_similarity([embedding1], [embedding2])[0][0]

    def find_closest_questions(self, new_question, data, num=3):
        """
            Search for similar questions
        """
        new_embedding, _ = self.generate_embedding(new_question)

        distances = [self.distance(new_embedding, item["question_embedding"]) for item in data]
        closest_indices = np.argsort(distances)[:num]

        return [(data[i]['question'], data[i]['sql']) for i in closest_indices]

    def create_vectordb_index(self):
        """
            Create FAISS DB vector database
        """
        embeddings_data = self.load_embeddings()

        query_embeddings = [ item['question_embedding'] for item in embeddings_data]
        print(len(query_embeddings))

        # query_array_updated = [[item['question'], item['sql']] for item in embeddings_data]
        embeddings_data_array = np.asarray(query_embeddings, dtype=np.float32)

        index = faiss.IndexFlatIP(len(query_embeddings[0]))
        index.add(embeddings_data_array)
        write_index(index, self.INDEX_FILE)

        # return index, query_array_updated

    def search_matching_queries(self, new_query):
        """
            Search for matching queries
        """

        embeddings_data = self.load_embeddings()
        query_array_updated = [[item['question'], item['sql']] for item in embeddings_data]

        nq_emb = self.embedding_model.get_embeddings([new_query])[0].values
        nq_emb_array = np.asarray([nq_emb], dtype=np.float32)

        index = read_index(self.INDEX_FILE)

        scores, ind = index.search(nq_emb_array, k=3)

        output_json = []
        for i in range(len(scores[0])):
            res = {}
            res['question'] = query_array_updated[ind[0][i]][0]
            res['sql'] = query_array_updated[ind[0][i]][1]
            output_json.append(res)

        return output_json

class PgSqlEmb():
    """
        class for interfacing with PostgreSQL
    """

    def __init__(self, proj_id,
                 loc,
                 pg_inst,
                 pg_db,
                 pg_uname,
                 pg_pwd,
                 pg_table='documents',
                 index_file='saved_index_pgdata'):        # Init function
        # self.EMBEDDING_FILE = "embeddings.json"

        self.PGPROJ = proj_id
        self.PGLOCATION = loc
        self.PGINSTANCE = pg_inst
        self.CONNSTRING = f"{self.PGPROJ}:{self.PGLOCATION}:{self.PGINSTANCE}"
        self.USER = pg_uname
        self.PWD = pg_pwd
        self.PGDB = pg_db
        self.PGTABLE = pg_table

        # self.INDEX_FILE = 'saved_index_pgdata'
        self.INDEX_FILE = f"{index_file}"
        self.embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        self.pool = self.getpool()
        print("PGSQL - class Initiated")

    def getconn(self) -> pg8000.dbapi.Connection:
        """
            Return DB connectionn string
        """
        connector = Connector()

        conn: pg8000.dbapi.Connection = connector.connect(
            self.CONNSTRING,
            "pg8000",
            user=self.USER,
            password=self.PWD,
            db=self.PGDB,
            ip_type=ip_type,
        )
        return conn

    def getpool(self):
        """
            Create SQL engine
        """
        pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=self.getconn,
            # ...
            )
        return pool

    def create_table(self):
        """
            Create table in PostgreSQL DB
        """
        sql_create = f"""CREATE TABLE IF NOT EXISTS {self.PGTABLE} (
             q_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
             question TEXT,
             sql TEXT,
             query_embedding TEXT
            );"""
        with self.pool.connect() as conn:
            conn.execute(sql_create)

    def empty_table(self, remove_index=True):
        """
            Clear all entries in the table
        """
        sql_clear = f'DELETE from {self.PGTABLE}'
        with self.pool.connect() as conn:
            conn.execute(sql_clear)
        if remove_index:
            try:
                os.remove(self.INDEX_FILE)
            except Exception:
                pass


    def insert_row(self,query, sql):
        """
            Adds rows to the PostgreSQL DB table
        """

        sql = sql.replace("'", "<sq>")
        sql = sql.replace('"', '<dq>')
        emb = self.embedding_model.get_embeddings([query])[0].values

        sql_ins = f"INSERT INTO {self.PGTABLE} \
                    (question, sql, query_embedding) \
                    values ('{query}', '{sql}', '{emb}')"
        with self.pool.connect() as conn:
            conn.execute(sql_ins)

        self.update_vectordb_index(query)

    def extract_data(self):
        """
            Returns the data in the table
        """
        sql_data = f'SELECT * FROM {self.PGTABLE}'
        with self.pool.connect() as conn:
            data = conn.execute(sql_data)
        return data

    def extract_pg_embeddings(self):
        """
            Returns the Embeddings saved in PG database
        """
        tmp = self.extract_data()
        df = DataFrame(tmp.fetchall())

        q_embed = df['query_embedding']
        len(q_embed)
        query_embeddings = [item.split(' ') for item in q_embed]
        new_array = []
        for elem in query_embeddings:
            new_row = []

            first_elem = elem[0].split('[')[1].split(',')[0]
            new_row.append(float(first_elem))
            for i in range(1, len(elem)-1):
                t_elem = elem[i].split(',')[0]
                new_row.append(float(t_elem))
            last_elem = elem[len(elem)-1].split(']')[0]
            new_row.append(float(last_elem))

            new_array.append(new_row)

        return df['question'], df['sql'], new_array

    def recreate_vectordb_index(self):
        """
            Recreate vector db from questions in PG DB
        """
        tmp = self.extract_data()
        df = DataFrame(tmp.fetchall())

        q_embed = df['query_embedding']
        print("Number of elements : ", len(q_embed))
        query_embeddings = [item.split(' ') for item in q_embed]
        new_array = []
        for elem in query_embeddings:
            new_row = []

            first_elem = elem[0].split('[')[1].split(',')[0]
            new_row.append(float(first_elem))
            for i in range(1, len(elem)-1):
                t_elem = elem[i].split(',')[0]
                new_row.append(float(t_elem))
            last_elem = elem[len(elem)-1].split(']')[0]
            new_row.append(float(last_elem))

            new_array.append(new_row)

        embeddings_data_array = np.asarray(new_array, dtype=np.float32)
        index = faiss.IndexFlatIP(len(query_embeddings[0]))
        index.add(embeddings_data_array)
        write_index(index, self.INDEX_FILE)

    def update_vectordb_index(self, query):
        """
            Update the Vector DB index file
        """
        emb = self.embedding_model.get_embeddings([query])[0].values
        new_array = [emb]

        # print(len(new_array), 'length of new array')

        embeddings_data_array = np.asarray(new_array, dtype=np.float32)

        # Read the index from stored index file
        try:
            index = read_index(self.INDEX_FILE)
        except:
            index = faiss.IndexFlatIP(len(new_array[0]))

        index.add(embeddings_data_array)
        write_index(index, self.INDEX_FILE)


    def search_matching_queries(self, new_query):
        """
            Search for closest matching queries
        """
        tmp = self.extract_data()
        df = DataFrame(tmp.fetchall())

        # q_embed = df['query_embedding']
        # query_embeddings = [item.split(' ') for item in q_embed]

        queries_array = df['question']
        sql_array = df['sql']

        nq_emb = self.embedding_model.get_embeddings([new_query])[0].values
        nq_emb_array = np.asarray([nq_emb], dtype=np.float32)

        try:
            print("Trying to read the index file", self.INDEX_FILE)
            index = read_index(self.INDEX_FILE)
        except Exception:
            self.recreate_vectordb_index()
            index = read_index(self.INDEX_FILE)

        scores, ind = index.search(nq_emb_array, k=3)

        output_json = []
        for i in range(len(scores[0])):
            res = {}
            tmp_sql = ''
            res['question'] = queries_array[ind[0][i]]

            tmp_sql = sql_array[ind[0][i]]
            tmp_sql = tmp_sql.replace('<dq>', '"')
            tmp_sql = tmp_sql.replace("<sq>", "'")
            res['sql'] = tmp_sql
            output_json.append(res)

        return output_json

if __name__ == '__main__':
    PGPROJ = "sl-test-project-363109"
    PGLOCATION = 'us-central1'
    PGINSTANCE = "nl2sql-test"
    PGDB = "test-db"
    PGTABLE = 'documents' #'myqueries'
    PGUSER = "postgres"
    PGPWD = "nl2sql-test"

    pge = PgSqlEmb(PGPROJ, PGLOCATION, PGINSTANCE, PGDB, PGUSER, PGPWD)
    # pge.recreate_vectordb_index()

    res = pge.search_matching_queries("What is the revenue for construction industry?")
    print(res)
    r2 = json.dumps(res)
    print(r2)
