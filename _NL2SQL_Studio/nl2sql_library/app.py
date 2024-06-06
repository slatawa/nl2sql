"""
    Main file serving the Executors modules exposing the APIs
    for Linear Executor, Chain of Thought executor, RAG Executor
    Updating user feedback etc
"""
# from nl2sql_lib_executors import NL2SQL_Executors
import re
import sys
import inspect
import json
import os

from utils.utility_functions import *

from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from google.cloud import bigquery
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

dataset_name = get_project_config()['config']['dataset'] #"zoominfo"

# bigquery_connection_string = "bigquery://sl-test-project-363109/zoominfo"
bigquery_connection_string = initialize_db(get_project_config()['config']['proj_name'],
                                           get_project_config()['config']['dataset'])

data_file_name = get_project_config()['config']['metadata_file']

metadata_cache_file = open(f"utils/{data_file_name}")
zoominfo_data = json.load(metadata_cache_file)
data_dictionary_read = {
            "zoominfo": {
                "description" : "This dataset contains information of Zoominfo Data\
                      with details on headquarters, marketing professionaals and\
                          providng tuition services.",
                "tables": 
                   zoominfo_data
            },
    }

@app.route("/")
def spec():
    """
        Default API Route
    """
    return json.dumps({"response":"Multi mode NL2SQL Generation library"})

@app.route('/api/executor/linear', methods=['POST'])
def linear_executor():
    """
        Invokes the Linear Executor
    """
    question = request.json['question']
    execute_sql = request.json['execute_sql']

    logger.info(f"Linear Execution engine for question : [{question}]")
    from nl2sql_lib_executors import NL2SQL_Executors
    try:
        nle = NL2SQL_Executors()
        res_id, sql = nle.linear_executor(question=question, data_dict=data_dictionary_read)
        sql_result = ""
        response_string = {"result_id": res_id,
                            "generated_query": sql,
                            "sql_result": sql_result,
                            "error_msg": ""}
        log_sql(res_id, question, sql, "Linear Executor", execute_sql)
        if execute_sql:
            try:
                result = execute_bq_query(sql)
                sql_result = result2nl(question, result)
                response_string = {"result_id": res_id,
                                    "generated_query": sql,
                                    "sql_result": sql_result,
                                    "error_msg": "", }
            except RuntimeError:
                logger.error('Runtime error while executing the Generated Query')
                response_string = {"result_id": res_id,
                                    "generated_query": sql,
                                     "sql_result": "",
                                     "error_msg": "Runtime error while executing the Generated Query", }
    except RuntimeError:
        logger.debug(f"Linear SQL Generation uncussessful : [{question}]")
        response_string = {"result_id": 0,
                            "generated_query": "",
                            "sql_result": "",
                            "error_msg":"Error encountered in Linear executor"}

    return json.dumps(response_string)

@app.route('/api/executor/cot', methods=['POST'])
def cot_executor():
    """
        Invokes the Chain of Thought executor
    """
    question = request.json['question']
    execute_sql = request.json['execute_sql']

    logger.info("CoT SQL Generation engine for question : [{question}]")
    from nl2sql_lib_executors import NL2SQL_Executors
    try:
        logger.info("CoT initialising the class")
        nle = NL2SQL_Executors()
        res_id, sql = nle.cot_executor(question=question, data_dict=data_dictionary_read)
        sql_result = ""
        response_string = {"result_id": res_id,
                            "generated_query": sql,
                            "sql_result": sql_result,
                            "error_msg": "" }
        sql2 = '\t'.join([line.strip() for line in sql])
        log_sql(res_id, question, str(sql2), "Chain of Thought Executor", execute_sql)
        if execute_sql:
            try:
                result = execute_bq_query(sql)
                sql_result = result2nl(question, result)
                response_string = {"result_id": res_id,
                                    "generated_query": sql,
                                    "sql_result": sql_result,
                                    "error_msg": "", }
            except RuntimeError:
                logger.error('Runtime error while executing the Generated Query')
                response_string = {"result_id": res_id,
                                    "generated_query": sql,
                                    "sql_result": "",
                                    "error_msg": "Runtime error while executing the Generated Query", }
    except RuntimeError:
        logger.debug(f"CoT SQL generation unsuccessful : [{question}]")
        response_string = {"result_id": 0,
                            "generated_query": "",
                            "sql_result": "",
                            "error_msg":"Error encountered in CoT executor"}

    return json.dumps(response_string)

@app.route('/api/executor/rag', methods=['POST'])
def rag_executor():
    """
        Invokes the RAG Executor 
    """
    question = request.json['question']
    execute_sql = request.json['execute_sql']

    logger.info("RAG SQL Generation engine for question : [{question}]")
    from nl2sql_lib_executors import NL2SQL_Executors
    try:
        nle = NL2SQL_Executors()
        res_id, sql = nle.rag_executor(question=question)
        # res_id, sql = nle.generate_query(question)
        print("res_id = ", res_id, "\ngen sql = ", sql, "\nExecute SQL = ", execute_sql)
        sql_result = ""
        response_string = {"result_id": res_id,
                            "generated_query": sql,
                            "sql_result": sql_result,
                            "error_msg": "" }
        log_sql(res_id, question, sql, "Rag Executor", execute_sql)
        if execute_sql:
            try:
                result = execute_bq_query(sql)
                sql_result = result2nl(question, result)
                response_string = {"result_id": res_id,
                                    "generated_query": sql,
                                    "sql_result": sql_result,
                                    "error_msg": "", }
            except RuntimeError:
                logger.error('Runtime error while executing the Generated Query')
                response_string = {"result_id": res_id,
                                    "generated_query": sql,
                                    "sql_result": "",
                                    "error_msg": "Runtime error while executing the Generated Query", }
    except RuntimeError:
        logger.debug(f"RAG SQL generation unsuccessful : [{question}]")
        response_string = {"result_id": 0,
                            "generated_query": "",
                            "sql_result": "",
                            "error_msg":"Error encountered in RAG executor"}

    return json.dumps(response_string)


@app.route('/projconfig', methods=['POST'])
def project_config():
    """
        Updates the Project Configuration details
    """
    project = request.json['proj_name']
    dataset = request.json['bq_dataset']
    metadata_file = request.json['metadata_file']
    config_project(project, dataset, metadata_file)

    return json.dumps({"response":"Project configuration successful"})

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    """
        Saves the data dictionary / metadata cache data
         received over HTTP request into a file 
    """
    print("file received")
    try:
        file = request.files['file']
        data = file.read()
        my_json = data.decode('utf8')
        data2 = json.loads(my_json)
        data_to_save = json.dumps(data2, indent=4)
        target_file = get_project_config()['config']['metadata_file']
        with open(f"utils/{target_file}", 'w') as outFile:
            outFile.write(data_to_save)
        return "successs"
    except RuntimeError:
        return json.dumps({"response":"Failed to upload file"})

@app.route('/userfb', methods=['POST'])
def user_feedback():
    """
        Updates the User feedback sent from UI
    """
    result_id = request.json['result_id']
    feedback = request.json['user_feedback']
    try:
        log_update_feedback(result_id, feedback)
        return json.dumps({"response":"Successfully updated user feedback"})
    except RuntimeError:
        return json.dumps({"response":"Failed to update user feedback"})

@app.route('/execsql', methods=['POST'])
def execute_sql_query():
    """
        Executes the query on BQ
    """
    sql = request.json['sql']
    result = execute_bq_query(sql)
    print("result = ", result)
    sql_result = result.to_dict() #orient="records")
    res_id = ""
    result_text = result2nl("", sql_result)
    response_string = {"result_id": res_id,
                        "generated_query": sql,
                        "sql_result": result_text,
                        "error_msg": "", }
    return json.dumps(response_string)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
