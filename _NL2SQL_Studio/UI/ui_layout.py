"""
    File describing the layout of the User Interface
    using Streamlit library widgets
"""
import os
from io import StringIO
# import time
import json


import streamlit as st
from streamlit_feedback import streamlit_feedback
from streamlit_modal import Modal
# import streamlit.components.v1 as components

import requests
from dotenv import load_dotenv

load_dotenv()

SHOW_SUCCESS = False

def define_session_variables():
    """
        Define the session variables once at the start of the app
    """
    st.session_state.messages = []
    st.session_state.question = ''
    st.session_state.new_question = False
    st.session_state.user_response = 0
    st.session_state.user_responded = False
    st.session_state.fb_count = 1
    st.session_state.refresh = True

    st.session_state.add_sample_question = False
    st.session_state.sample_question = ''
    st.session_state.sample_sql = ''
    st.session_state.add_question_status = False
    st.session_state.result_id = "  "

q_s_modal = Modal(
        "Query Selector", 
        key="qsm",
        # Optional
        padding=10,    # default value
        max_width=700  # default value
    )

pc_modal = Modal('Project Configuration', key='pcm', padding=10, max_width=545)
qa_modal = Modal('Sample QnA', key='qam', padding=10, max_width=545)
info_modal = Modal('Success !!', key='info', padding=2, max_width=200)

def define_layout():
    """
        Streamlit UI layout with page configuration, styles,
        widgets, main screen and sidebar, etc
    """
    st.set_page_config(page_title='NL2SQL new Studio',
                       page_icon="📊",
                       initial_sidebar_state="expanded",
                       layout='wide')
    st.markdown("""
            <style>
                .block-container {
                        padding-top: 0.25rem;
                        padding-bottom: 0rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
            [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
            [data-testid=stContainer] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
                border: 2px;
                min-height: 30%;
                max-height: 50%;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar.container() :
        column_1, column_2 = st.columns(2)
        with column_1:
            st.image('google.png')
        with column_2:
            st.write('v0.2')

    with st.sidebar.container(height=140):
        st.session_state.model = st.radio('Pick your Model',
                                          ['Linear Executor',
                                           'Rag Executor',
                                            "Chain of Thought"])
    with st.sidebar.expander("Configuration Settings"):
        proj_conf = st.button("Project Configuration")
        rag_input = st.button("Questions  &  Queries", disabled=True)

    with st.sidebar.container(height=60):
        st.session_state.execution = st.checkbox("Generate and Execute", disabled=True)

    # Main Page
    st.image('solid_g-logo-2.png')

    with st.container():
        column_1, column_2, column_3 = st.columns([0.25, 0.85, 0.1])

        with column_3:
            st.markdown('',
                        help="""For the purpose of this demo we have setup a demo project with id
                         'sl-test-project-363109' created a dataset in BigQuery named 'zoominfo'.
                         This dataset contains 3 tables with information that is a subset of
                         Zoominfo Data Cubes.  This a the default dataset to generate SQLs from 
                         related natural language statements.  For custom query generation, 
                         specify the Project ID, Dataset and Metadata of tables in the 
                         Configuration settings in the Sidebar panel"""  )

    inp_container = st.container()
    with inp_container:
        column_1, column_2 = st.columns([0.86, 0.14])
        with column_2:
            q_s = st.button('Sample Queries', key='qs_button')
        with column_1:
            if question := st.chat_input("Enter your question here"):
                _message_queue(question)
                st.session_state.question = question
                st.session_state.new_question = True
                st.session_state.user_responded = False

    # fb_container = st.container()
    # st.session_state.fc = fb_container
    # get_feedback()

    msg_container_main = st.container(height=425)
    with msg_container_main:
        column_1, column_2 = st.columns([0.90, 0.10])
        with column_1:
            msg_container = st.container()
        with column_2:
            fb_container = st.container()

    st.session_state.fc = fb_container
    get_feedback()


    st.markdown("<p style='text-align: center; font-style: italic; font-size: 0.75rem;'>\
                The SQL generated by this tool may be inaccurate or incomplete. \
                Always review and test the code before executing it against your database.</p>",
                unsafe_allow_html=True)

    st.session_state.ic = inp_container
    st.session_state.mc = msg_container


    # conditional rendering
    if q_s:
        q_s_modal.open()

    if q_s_modal.is_open():
        with q_s_modal.container():
            # st.title("Copy any sample question")
            st.code('What is the revenue of construction industry?')
            st.code("What are the top 5 industries in terms of revenue \
for companies having headquarters in California?")
            st.code("What is the total number of employes providing tuitions\
that are there in the company?")
            st.code('What is the revenue generated by sales agents for Manufacturing industry?')
            st.code('Which county in California serves most number of industries?')

            if st.button("Close"):
                q_s_modal.close()


    if proj_conf:
        pc_modal.open()

    if rag_input:
        qa_modal.open()

    if qa_modal.is_open():
        with qa_modal.container():
            samp_question = st.text_input('Enter sample question')
            samp_sql = st.text_input(("Enter corresponding SQL"))
            if st.session_state.add_question_status:
                st.success("Success ! Question added to DB ")
            if st.button('Add question'):
                add_question_to_db(samp_question, samp_sql)
                info_modal.open()
                qa_modal.close(True)



    if pc_modal.is_open():
        with pc_modal.container():
            project = st.text_input('Mention the GCP project name')
            dataset = st.text_input('Specify the BigQuery dataset name')
            uploaded_file = st.file_uploader("Choose the Metadata Cache file")
            if st.button("Save configuration"):
                if uploaded_file is not None:
                    # To read file as bytes:
                    url = os.getenv('EXECUTORS')
                    # To convert to a string based IO:
                    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

                    # To read file as string:
                    string_data = stringio.read()
                    files = {'file': (uploaded_file.name, string_data)}
                    body = {"proj_name": project,
                            "dataset":dataset,
                            "metadata_file":uploaded_file.name}
                    headers={"Content-type": "application/json"}
                    # url = "http://localhost:5000"
                    res = requests.post(url=url+"/projconfig",
                                        data=json.dumps(body),
                                        headers=headers,
                                        timeout=None)
                    res = requests.post(url=url+"/uploadfile",
                                        files=files,
                                        timeout=None)

                pc_modal.close()

    # selection = st.session_state.question
    # st.session_state.ic = inp_container
    # st.session_state.mc = msg_container
    st.session_state.add_question_status = False

def _submit_feedback(user_response):
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }
    print(score_mappings["thumbs"][user_response['score']])
    st.session_state.user_response = score_mappings["thumbs"][user_response['score']]
    st.session_state.user_responded = True
    print("Response state = ", st.session_state.user_responded)
    return user_response

def get_feedback():
    """
        Position the Thumbs Up/Down User feedback widget 
    """
    # print("initialing the feedback widget")
    i = 0
    num_msgs = len(st.session_state.messages)
    with st.session_state.fc:
        for i in range(1, num_msgs):
            fb_cont = "c"+str(i)
            fb_cont = st.container(height=70, border=False)
            i+=1
            with fb_cont:
                st.write('')

        if feedback := streamlit_feedback(feedback_type="thumbs",
                                          on_submit=_submit_feedback,
                                          key='fbkey'+str(st.session_state.fb_count)):
            print("Feedback == ", st.session_state.get('feedback'))
            del st.session_state['fbkey'+str(st.session_state.fb_count)]
            # st.session_state.pop('fbkey'+str(st.session_state.fb_count))
            st.session_state.fb_count += 1
            # print("Setting the refresh state to true ")
            st.session_state.refresh = True

def _message_queue(question):
    """
        Append user queries and system responses to the message queue
    """
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant",
                                      "content": """Fetching results...
                                      [![Loading](https://cdn3.emoji.gg/emojis/7048-loading.gif)](https://emoji.gg/emoji/7048-loading)"""})

def add_question_to_db(sample_question, sample_sql):
    """
        Add Sample questions and corresponding SQLs to the
        PostgreSQL DB
    """
    url = os.getenv('ADD_QUESTION')
    # print("Adding new question", sample_question, sample_sql)
    data = { "question": sample_question, "sql": sample_sql}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # print(url)
    resp = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=None)
    SHOW_SUCCESS = True
    st.session_state.add_question_status = True
