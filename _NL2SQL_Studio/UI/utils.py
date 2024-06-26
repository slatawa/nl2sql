"""
    Utility functions for the NL2SQL Studio User Interface written in Streamlit
    This module contains the functions required to invoke the APIs, track user
    actions and other support tasks 
"""

import os
import time
# from io import StringIO
import json
# from typing import Annotated
import configparser

import streamlit as st
from streamlit_feedback import streamlit_feedback
from streamlit.components.v1 import html
# from streamlit_modal import Modal

from dotenv import load_dotenv
from loguru import logger

from google.auth.transport import requests
# import google.auth.transport.requests
import requests

# from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordBearer

from jose import jwt



load_dotenv()

# show_success = False

# API Calls
def default_func(prompt):
    """
        Test function that returns a reversed question output instead of executor
    """
    time.sleep(3)
    sql = prompt[::-1]
    st.session_state.messages[-1]['content'] = sql
    st.session_state.new_question = False
    st.rerun()
    st.session_state.refresh = True
    return sql

def call_generate_sql_api(question, endpoint):
    """
        Common SQL generation function
    """
    api_url = os.getenv('EXECUTORS')
    api_endpoint = f"{api_url}/{endpoint}"
    logger.info(f"Invoking API : {api_endpoint}")
    data = {"question": question, "execute_sql":st.session_state.execution}
    headers = {"Content-type": "application/json" }
    logger.info(f"Provided parameters are : Data = {data}")
    api_response = requests.post(api_endpoint,
                                 data=json.dumps(data),
                                 headers=headers,
                                 timeout=None)
    exec_result = ""
    try:
        resp = api_response.json()
        sql = resp['generated_query']
        st.session_state.result_id = resp['result_id']
        exec_result = resp['sql_result']
    except RuntimeError:
        sql = "Execution Failed ! Error encountered in RAG Executor"

    logger.info(f"Generated SQL = {sql}")
    logger.info(f"Generation ID = {st.session_state.result_id}")
    return sql, exec_result



def rag_gen_sql(question):
    """
        SQL Generation using the RAG Executor
    """
    logger.info("Invoking the RAG Executor")
    sql, exec_result = call_generate_sql_api(question, 'api/executor/rag')
    st.session_state.messages[-1]['content'] = sql + \
                                            exec_result if st.session_state.execution else sql
    st.session_state.new_question = False
    st.rerun()
    return sql

def cot_gen_sql(question):
    """
        SQL Generation using the Chain of Thought executor
    """
    logger.info("Invoking the Chain of Thought Executor")
    sql, exec_result = call_generate_sql_api(question, 'api/executor/cot')

    st.session_state.messages[-1]['content'] = sql + \
                                            exec_result if st.session_state.execution else sql
    st.session_state.new_question = False
    st.rerun()
    return sql

def linear_gen_sql(question):
    """
        SQL Generation using the Linear executor
    """
    logger.info("Invoking the Linear Executor")
    sql, exec_result = call_generate_sql_api(question, 'api/executor/linear')

    st.session_state.messages[-1]['content'] = sql + \
                                            exec_result if st.session_state.execution else sql
    st.session_state.new_question = False
    st.rerun()
    return sql

# Utility functions

def submit_feedback(user_response):
    """
        Function to capture the score of Feedback widget click
    """
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }
    logger.info(f"Score Mapping = {score_mappings['thumbs'][user_response['score']]}")
    st.session_state.user_response = score_mappings["thumbs"][user_response['score']]
    st.session_state.user_responded = True
    logger.info(f"User Response state = {st.session_state.user_responded}")
    return user_response


def message_queue(question):
    """
        Append user queries and system responses to the message queue
    """
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant",
                                      "content": """Fetching results...
                                      [![Loading](https://cdn3.emoji.gg/emojis/7048-loading.gif)](https://emoji.gg/emoji/7048-loading)"""})

def get_feedback():
    """
        Position the Thumbs Up/Down User feedback widget 
    """
    i = 0
    num_msgs = len(st.session_state.messages)
    with st.session_state.fc:
        for i in range(1, num_msgs):
            fb_cont = "c"+str(i)
            fb_cont = st.container(height=70, border=False)
            with fb_cont:
                st.write('')
                if "User feedback captured" in st.session_state.messages[i]['content']:
                    fb_cont2 = "c"+str(i)+"2"
                    fb_cont2 = st.container(height=70, border=False)
                    with fb_cont2:
                        st.write('')
            i+=1

        if feedback := streamlit_feedback(feedback_type="thumbs",
                                          on_submit=submit_feedback,
                                          key='fbkey'+str(st.session_state.fb_count)):
            del st.session_state['fbkey'+str(st.session_state.fb_count)]
            st.session_state.fb_count += 1
            st.session_state.refresh = True

def add_question_to_db(sample_question, sample_sql):
    """
        Add Sample questions and corresponding SQLs to the
        PostgreSQL DB
    """
    url = os.getenv('ADD_QUESTION')
    logger.info(f"Adding {sample_question} and {sample_sql} to DB")

    data = { "question": sample_question, "sql": sample_sql}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    _ = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=None)
    st.session_state.add_question_status = True



# Authentication functions
# GOOGLE_CLIENT_ID = ''
# GOOGLE_CLIENT_SECRET = ''
# GOOGLE_REDIRECT_URI = ''


def open_url(url):
    """
        Open the given URL 
    """
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)


def init_auth():
    """
        Authentication Initialisation function
    """
    logger.info("Initialising Authentication process")
    # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    config = configparser.ConfigParser()
    config.read('config.ini')
    # GOOGLE_CLIENT_ID = config['DEFAULT']['GOOGLE_CLIENT_ID']
    # GOOGLE_CLIENT_SECRET = config['DEFAULT']['GOOGLE_CLIENT_SECRET']
    google_redirect_uri = config['DEFAULT']['GOOGLE_REDIRECT_URI']

    logger.info(f"Redirect URI = {google_redirect_uri} ")

def login_user():
    """
        Trigger Logging in
    """
    init_auth()
    logger.info("Authenticating...")
    view_login_google()


def view_login_google():
    """
        Navigating to Authentication URL
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    google_client_id = config['DEFAULT']['GOOGLE_CLIENT_ID']
    # GOOGLE_CLIENT_SECRET = config['DEFAULT']['GOOGLE_CLIENT_SECRET']
    google_redirect_uri = config['DEFAULT']['GOOGLE_REDIRECT_URI']

    auth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={google_client_id}&redirect_uri={google_redirect_uri}&scope=openid%20profile%20email&access_type=offline"
    logger.info(f"URL to authenticate = {auth_url}")
    open_url(auth_url)
    # return json.dumps(resp_str)


def view_auth_google(code):
    """
        Retrieve the Code and Tokens
    """

    logger.info("Extracting the Code and Generating the Tokens")
    logger.info(f"Query Parameters - {st.query_params}")
    config = configparser.ConfigParser()
    config.read('config.ini')

    google_client_id = config['DEFAULT']['GOOGLE_CLIENT_ID']
    google_client_secret = config['DEFAULT']['GOOGLE_CLIENT_SECRET']
    google_redirect_uri = config['DEFAULT']['GOOGLE_REDIRECT_URI']


    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": google_client_id,
        "client_secret": google_client_secret,
        "redirect_uri": google_redirect_uri,
        "grant_type": "authorization_code",
    }
    logger.info(f"Auth info =, {data}")
    # try:
    #     logger.info("First attempt - using requests.Request()")
    #     request = google.auth.transport.requests.Request()
    #     response = request.post(token_url, data=data)
    #     access_token = response.json().get("access_token")
    #     # print("Access token = ", access_token)
    #     logger.info(f"Access token = {access_token}")
    # except Exception:
    #     logger.error("requests.Request() did not succeed")
    #     # print()

    try:
        # print("Second attempt - using requests library")
        logger.info("Second Attempt - using requests library itself")

        response = requests.post(token_url, data=data, timeout=None)
        # print("Respoiinse =", response.json())
        logger.info(f"Auth response = {response.json()}")
        access_token = response.json().get("access_token")
        id_token = response.json().get("id_token")
        logger.info(f"Access token = {access_token}")
        logger.info(f"ID Token = {id_token}")

    except Exception:
        logger.error("Authentication via Requests library  failed")

    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                             headers={"Authorization": f"Bearer {access_token}"}, timeout=None)
    logger.info(f"Decoded User info : {user_info.json()}")
    # return user_info.json()

    return json.dumps({ "token": id_token, "access_token": access_token})

def view_get_token(token):
    """
        Retrieve the token
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    google_client_secret = config['DEFAULT']['GOOGLE_CLIENT_SECRET']

    logger.info("Retrieving token")
    algorithm = jwt.get_unverified_header(token).get('alg')
    logger.info("Algorithms to use : {algorithm}")
    try:
        response = jwt.decode(token, google_client_secret, algorithms=algorithm)
        logger.info("Decoded token=", response)
        return response
    except Exception:
        logger.error("Something went wrong while decooding")
        return "Decode error due to Algorithmm mismatch"
    # return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["RS256"])
