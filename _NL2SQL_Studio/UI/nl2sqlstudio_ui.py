"""
    Main UI file to render the Streamlit UI on browser
"""
import os
import json
import time
import requests
from dotenv import load_dotenv

import streamlit as st
# from streamlit_feedback import streamlit_feedback
# from ui_layout import * # define_layout
from ui_layout import define_session_variables, define_layout, get_feedback


load_dotenv()

if 'init' not in st.session_state:
    define_session_variables()
    st.session_state.init = False

define_layout()

mc = st.session_state.mc
fc = st.session_state.fc
Result_Id = ''

def default_func(prompt):
    """
        Test function that returns a string output instead of executor
    """
    time.sleep(3)
    rev = prompt[::-1]

    api_url = os.getenv('EXECUTORS')
    api_endpoint = f"{api_url}/"
    # print(api_endpoint, st.session_state.execution)
    api_response = requests.get(api_endpoint, timeout=None)
    try:
        response = api_response.json()
        sql = response['response']
    # except:
    except RuntimeError:
        sql = "Error encountered in  Executor"
    st.session_state.messages[-1]['content'] = sql
    st.session_state.new_question = False
    st.rerun()
    st.session_state.refresh = True
    return rev

def rag_gen_sql(question):
    """
        SQL Generation using the RAG Executor
    """
    # api_url = os.getenv('EXECUTORS')
    # api_endpoint = f"{api_url}/api/executor/rag"
    # data = {"question": question, "execute_sql":st.session_state.execution}
    # headers = {"Content-type": "application/json", }
    # api_response = requests.post(api_endpoint,
    #                              data=json.dumps(data),
    #                              headers=headers,
    #                              timeout=None)
    # try:
    #     resp = api_response.json()
    #     sql = resp['generated_query']
    #     # Result_Id = resp['result_id']
    #     st.session_state.result_id = resp['result_id']
    #     exec_result = resp['sql_result']
    # # except:
    # except RuntimeError:
    #     sql = "Execution Failed ! Error encountered in RAG Executor"
    print("RAG Execution ", question)
    sql = "RAG based SQL Generation... Coming soon !!"
    exec_result = ""
    st.session_state.messages[-1]['content'] = sql + \
                                            exec_result if st.session_state.execution else sql
    st.session_state.new_question = False
    st.rerun()
    return sql

def cot_gen_sql(question):
    """
        SQL Generation using the Chain of Thought executor
    """
    api_url = os.getenv('EXECUTORS')
    api_endpoint = f"{api_url}/api/executor/cot"
    data = {"question": question, "execute_sql":st.session_state.execution}
    headers = {"Content-type": "application/json"}

    api_response = requests.post(api_endpoint,
                                 data=json.dumps(data),
                                 headers=headers,
                                 timeout=None)
    try:
        # print("Cot response", api_response.json())
        response = api_response.json()
        sql = response['generated_query']
        # Result_Id = resp['result_id']
        st.session_state.result_id = response['result_id']
        exec_result = response['sql_result']
    # except:
    except RuntimeError:
        sql = "Execution Failed ! Error encountered in COT Executor"

    # sql = "RAG Generated sql is given for the questionn :" + question
    st.session_state.messages[-1]['content'] = sql + \
                                            exec_result if st.session_state.execution else sql
    st.session_state.new_question = False
    st.rerun()
    return sql

def linear_gen_sql(question):
    """
        SQL Generation using the Linear executor
    """
    api_url = os.getenv('EXECUTORS')
    api_endpoint = f"{api_url}/api/executor/linear"
    data = {"question": question, "execute_sql":st.session_state.execution}
    headers = {"Content-type": "application/json"}
    api_response = requests.post(api_endpoint,
                                 data=json.dumps(data),
                                 headers=headers,
                                 timeout=None)
    try:
        # print("Api response = ", api_response.json())
        response = api_response.json()
        sql = response['generated_query']
        # Result_Id = resp['result_id']
        st.session_state.result_id = response['result_id']
        exec_result = response['sql_result']
    # except:
    except RuntimeError:
        sql = "Execution failed ! Error encountered in Linear Executor"
    # sql = "Linear Exeuctor Generated sql is given for the questionn :" + question
    st.session_state.messages[-1]['content'] = sql + \
                                            exec_result if st.session_state.execution else sql
    st.session_state.new_question = False
    st.rerun()
    return sql

def redraw():
    """
        Trigger the re-rendering of the UI
    """
    # st.mc.empty()
    with mc:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if 'new_question' in st.session_state:
    redraw()
    st.session_state.refresh = False
    if st.session_state.new_question:
        if st.session_state.model == 'None':
            default_func(st.session_state.question)
        elif st.session_state.model == 'Linear Executor':
            # print("Linear Executor")
            linear_gen_sql(st.session_state.question)
        elif st.session_state.model == 'Chain of Thought':
            # print("Chain of Thought executor")
            cot_gen_sql(st.session_state.question)
        else:
            # print("Rag Executor")
            rag_gen_sql(st.session_state.question)



if st.session_state.user_responded:
    st.session_state.user_responded = False
    resp = st.session_state.messages[-1]['content']
    user_feedback = 'True' if st.session_state.user_response == 1 else 'False'
    if user_feedback == 'True':
        # added_text = '<span style="font-size:10px; font: arial">\
        # ${\color{green}User feedback captured}$</span>'
        infoText = ':green[👍 User feedback captured ]'
    else:
        # added_text = "<p style='color:red;'>User feedback Captured</p>"
        infoText = ':red[👎 User feedback captured ]'

    st.session_state.messages[-1]['content'] = resp + " \n\n" +  infoText
    # redraw()
    # st.rerun
    url = os.getenv('EXECUTORS') + '/userfb'
    data = { "result_id": st.session_state.result_id , "user_feedback": user_feedback}
    print("data= ", data)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    print(url)
    resp = requests.post(url=url,
                         data=json.dumps(data),
                         headers=headers,
                         timeout=None)

    st.session_state.refresh = True
    get_feedback()



if st.session_state.refresh:
    # redraw()
    st.rerun()
else:
    st.session_state.refresh = True
    # st.rerun()
