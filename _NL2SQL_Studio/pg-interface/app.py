# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    Main file to serve the APIs
"""
import sys
import inspect
import json

import os

from flask import Flask, request
from flask_cors import CORS
from google.cloud import bigquery
from dotenv import load_dotenv
from loguru import logger
from nl2sql_query_embeddings import PgSqlEmb

load_dotenv()



currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# ask_objs = get_ask_bqs()


bq_client = bigquery.Client()

PGPROJ = "sl-test-project-363109"
PGLOCATION = 'us-central1'
PGINSTANCE = "nl2sql-test"
PGDB = "test-db"
PGTABLE = 'documents' #'myqueries'
PGUSER = "postgres"
PGPWD = "nl2sql-test"

@app.route("/")
def spec():
    """
        Default route
    """
    msg = { "response":"NL2SQL Library PostgreSQL interface"}
    return json.dumps(msg)

@app.route('/api/table/create', methods=['POST'])
def create_pgtable():
    """
        Create table in the PostgreSQL DB
    """
    table_name = request.json['table_name']

    try:
        pge = PgSqlEmb(PGPROJ, PGLOCATION, PGINSTANCE, PGDB, PGUSER, PGPWD, pg_table=table_name)
        pge.create_table(table_name)
        return {"success"}
    except:
        return {"failed"}

@app.route('/api/record/create', methods=['POST'])
def create_pgtable_record():
    """
        Insert record with Question and MappedSQL in the Table  
    """
    question = request.json['question']
    mappedsql = request.json['sql']
    logger.info(f"Input data : {question} and {mappedsql}")
    try:
        pge = PgSqlEmb(PGPROJ, PGLOCATION, PGINSTANCE, PGDB, PGUSER, PGPWD)
        pge.insert_row(question, mappedsql)
        return "Successfully inserted record"
    except:
        return "Unable to insert record"

@app.route('/api/similar_questions', methods=['POST'])
def similar_questions():
    """
        Returns 3 most similar questions to the given question
    """
    question = request.json['question']
    try:
        pge = PgSqlEmb(PGPROJ, PGLOCATION, PGINSTANCE, PGDB, PGUSER, PGPWD)
        results = pge.search_matching_queries(question)
        return_val = json.dumps(results)
        return return_val
    except:
        return "Similar questions not found"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
