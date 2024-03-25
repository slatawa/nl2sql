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

import datetime
import os

import pandas
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()
from nl2sql_textbison_geminipro.predict_nl2sql_geminipro import generate_sql_geminipro
from nl2sql_textbison_geminipro.predict_nl2sql_textbison import generate_sql_textbison1

from text2sql_prediction.predict_nl2sql import call_gen_sql, get_ask_bqs
from text2sql_prediction.utils import getgenai_response, parse_and_modify_query
import re

from sql_gen.final_lib.nl2sql_src.nl2sql_generic import Nl2sqlBq_rag



app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# ask_objs = get_ask_bqs()


bq_client = bigquery.Client()


@app.route('/api/qa', methods=['POST'])
def genai_qa():

    question = request.json['question']
    unique_id = request.json['unique_id']

    dataset_id = 'qnadb'
    # For this sample, the table must already exist and have a defined schema
    table_id = 'question_answers'

    meta_data_json_path = "./sql_gen/final_lib/cache_metadata/metadata_cache.json"
    project_id = os.environ['PROJECT_ID']
    nl2sqlbq_client = Nl2sqlBq_rag(project_id=project_id,
                           dataset_id=dataset_id,
                           metadata_json_path = meta_data_json_path, #"../cache_metadata/metadata_cache.json",
                           model_name="text-bison"
                           # model_name="code-bison"
                          )
    table_identified = nl2sqlbq_client.table_filter(question)
    print("Table Identified - app.py = ", table_identified)

    PGPROJ = os.environ['PROJECT_ID'] #"cdii-poc"
    PGLOCATION = os.environ['REGION'] #'us-central1'
    PGINSTANCE = os.environ['PG_INSTANCE'] #"cdii-demo-temp"
    PGDB = os.environ['PG_DB'] #"demodbcdii"
    PGUSER = os.environ['PG_USER'] #"postgres"
    PGPWD = os.environ['PG_PWD'] #"cdii-demo"

    nl2sqlbq_client.init_pgdb(PGPROJ, PGLOCATION, PGINSTANCE, PGDB, PGUSER, PGPWD)
    sql_query = nl2sqlbq_client.text_to_sql_fewshot(question)
    print("Generated query == ", sql_query)
    
    parameters_textbison1 = {
        "temperature": 0.0,
        "max_output_tokens": 1024,
        "top_p": 0,
        "top_k": 1,
    }

    # result_sql = generate_sql_geminipro(question,parameters_textbison1)
    try:
        result_sql = sql_query
        # result_sql = generate_sql_textbison1(question, parameters_textbison1)
        print('Output by textbison', result_sql)
        model_name = 'text-bison'
        # if not result_sql:
        # result_sql = generate_sql_geminipro(question,parameters_textbison1)
        # print('Output by gemini pro', result_sql)
        # model_name = 'gemini-pro'
        if not result_sql:
            result_sql = call_gen_sql(ask_objs, question)
            print('Output by model.', result_sql)
            model_name = 'text-bison'
        print("1>>>", result_sql)

        print('questtion>>', question)
        # try:
        result_sql = re.sub('```', '', result_sql)
        result_sql = re.sub('sql', '', result_sql)
        QUERY = (result_sql)
        print('Query - app.py = ', QUERY)
        query_job = bq_client.query(QUERY)  # API request
        rows = query_job.result()
        df = pandas.read_gbq(result_sql, dialect="standard")
        print("Dataframe = ", df)
        print("rows>>>", rows)

        # print("rows>>>",len(rows))
        # try:
        resp = getgenai_response(model_name, question, str(
            df.to_json(orient='records')), parameters_textbison1)

    # resp = getgenai_response(question, '12365')

        print("Final result =>  ", resp)
        if resp:
            result_data = resp
        else:
            result_data = "No response from GenAi."
        ##
        table_ref = bq_client.dataset(dataset_id).table(table_id)
        table = bq_client.get_table(table_ref)
        rows_to_insert = [(unique_id, result_data, result_sql,
                           question, datetime.datetime.now(), True)]
        errors = bq_client.insert_rows(table, rows_to_insert)
        query_job.result()  # Waits for statement to finish
        # except:
        # resp = "No response from GenAi."
        # print("errors")
        return jsonify({'unique_id': unique_id, 'question': question, 'error': '', 'status': 200})
    except Exception as error:
        return jsonify({'unique_id': unique_id, 'question': question, 'error': 'Error: {}'.format(str(error)), 'status': 500})


@app.route("/api/display")
def genai_display():
    QUERY = ("SELECT * FROM `qnadb.question_answers` order by created_date desc")
    query_job = bq_client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    uid = ''
    que = ''
    result = []
    for row in rows:
        dt = {'unique_id': row.unique_id, 'data': row.result_data, 'sql': row.result_sql,
              'question': row.question, 'created_date': row.created_date, 'status': row.status}
        result.append(dt)
    return jsonify(result)


@app.route("/")
def spec():
    return "Welcome to EY Analytics"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
