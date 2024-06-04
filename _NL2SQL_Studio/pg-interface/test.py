"""
    PostgreSQL Interface Test case file
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


URL = "https://pginterface-dot-sl-test-project-363109.uc.r.appspot.com/"
URL2 = os.getenv('add_question')

def insert_record(question, sql):
    """
        Insert record test case
    """

    data = { "question": question, "sql": sql}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resp = requests.post(url=URL2, data=json.dumps(data), headers=headers, timeout=None)
    # r = resp.json()
    print(resp)


def getapi():
    """
        Sample test
    """
    resp = requests.get(URL, timeout=None)
    # r = resp.json()
    print(resp)

if __name__ == '__main__':
    QUESTION = "What are the top 10 industries having revenue greater than 1 million?"
    SQL = 'select * from table1 where industry="pharma"'
    getapi()
    insert_record(QUESTION, SQL)
