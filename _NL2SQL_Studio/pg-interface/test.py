import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


url = "https://pginterface-dot-sl-test-project-363109.uc.r.appspot.com/"
# url2 = "https://pginterface-dot-sl-test-project-363109.uc.r.appspot.com/api/record/create"
url2 = os.getenv('add_question')

print(url2)
def insert_record(question, sql):
    
    data = { "question": question, "sql": sql}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resp = requests.post(url=url2, data=json.dumps(data), headers=headers)
    # r = resp.json()
    print(resp)


def getapi():
    resp = requests.get(url)
    # r = resp.json()
    print(resp)

question = "What are the top 10 industries having revenue greater than 1 million?"
sql = 'select * from table1 where industry="pharma"'

getapi()

insert_record(question, sql)