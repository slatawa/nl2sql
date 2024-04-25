# NL2SQL Generic Library


## Introduction

NL2SQL Library allows you to interact with your databases/datasets in BQ by leverating Vertex AI LLMs on the Google Cloud. It helps generating SQL query statements from natural language questions.  Salient features of the library are

1. Filter for tables required to generate the SQL for a given natural language statement
2. Zero-shot or Few-shot prompting using vector embeddings and searching for closest matching queries
3. Multi-turn SQL generation while retaining the context of the original statement
4. Support for JOINs
5. Auto-verify generated SQL, execute and return results in natural language
6. Chat based web UI for interacting with the library


[Prerequisities](prerequisites.md)

[Modules and Descriptions](under_the_hood.md)

[Deployment](deployment.md)




## Starting Front-end and Back-end modules

### Launching the back-end locally

1. Navigate to the `py-backend-api` directory:
   ```bash
   cd py-backend-api
   ```

2. Create environment: 
  - Use Python 3.10 (recommended using `pyenv` to install and manage Python versions)
  - `python3 -m venv venv`
  - `source venv/bin/activate`
  
3. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Backend server locally:
   ```bash
   flask run
   ```
   OR
   ```bash
   python app.py
   ````

   By default, the app will be running on [http://localhost:5000/](http://localhost:5000/).


### Launching the front-end locally

Follow these steps to start the development server on your local machine:

1. Navigate to the `webapp` directory:

   ```bash
   cd webapp
   ```
2. Install the necessary dependencies:
   ```bash
   npm i
   ```
3. Run the UI server locally:
   ```bash
   npm run dev
   ```
   By default, the app will be running on [http://localhost:5173/](http://localhost:5173/).


## Deploying the Application on App Engine

### Deploying Back-end service

To deploy the application on App Engine, ensure you follow these prerequisites and steps:

1. **Permissions**: Make sure you have the required IAM permissions before deploying the app.

2. **Update `app.yaml`**: If necessary, update the `app.yaml` file in the `py-backend-api` directory to reflect any specific deployment configurations.

3. **Project ID**: Set the project ID.
    ```
    gcloud config set project [PROJECT_ID]
    ```
4. Deploy the app on App Engine:
   ```bash
   gcloud app deploy
   ```
5. Use below command to get/launch the deployed app url. For example
    ```bash
    gcloud app browse --service <servicename>
    ```


### Deploying Front-end service

To deploy the webapp application on App Engine, ensure you follow these prerequisites and steps:

1. **Permissions**: Make sure you have the required IAM permissions before deploying the app.

2. **Update `app.yaml`**: If necessary, update the `app.yaml` file in the `webapp` directory to reflect any specific deployment configurations.

3. **Project ID**: Verify that the deploy command in `package.json` is pointing to the correct project ID.

4. Deploy the app on App Engine:
   ```bash
   npm run deploy
   ```

5. Use below command to get/launch the deployed app url. For example
    ```bash
    gcloud app browse --service <webapp>
    ```
    <webapp> is the deployed service name



## API Integration

### API Endpoints 

**/api/sqlgen** is the end-point that is to be used to generate the SQL.  The natural lanaugage question is to be submitted to this endpoint via a POST Https method in Json format.  Required field : "**question**"

**/api/display** is used to display the latest question and the generated SQL for that question.  If there is an error in generaing the SQL for a given question, this API returns the SQL for the question if it exists in its list


**/api/table/create** is the end-point to create a table in the PostGreSql DB.  Required field : "**table_name**"

**/api/record/create** is the end-point to insert rows into the PostgreSQL table.  The inserted rows are example questions and corresponding SQLs that can be retrieved using similarity analysis for few-shot prompting in SQL generation. 
Required fields : "**question**", "**sql**"



# Generatiing SQL from Natural statements using the library

## Using HTTP APIs

### Using PostMan client or other HTTP Clients

Steps to generate SQL
1. In HTTP client (for ex. Postman), specify the URL (endpoint) and the select the method as POST
2. Click on Body, select 'raw' type and select JSON as the type
3. specify {"question":"<youur question>, "unique_id":"<unique id - can be anyreference id>}
4. Click Send

### Using Python requests library

```code
import requests
import json

url_sql_gen = '<your quuestion here>/api/sqlgen'
url_display = '<your quuestion here>/api/display'

uniqueid="unique id -- can be random"
question = <your question>

data = {"question": question, "unique_id":uniqueid}
headers={"Content-type":"application/json", "Accept":"text/plan"}
resp = requests.post(url_sql_gen, data=json.dumps(data), headers=headers)

if resp.status == 200:
    resp = requests.get(url_display)
    print('Generated SQL - ', resp[0]['sql])

```


## Using Webapp interface

1. Launch the Web interface (either locally or in App engine - see above)
2. Type your question in the Question input field and click Submit
3. Generated SQL will be displayed below the question input field

## Using Jupyter notebook

### Normal queries

1. Create a new Jupyter notebook or make a copy of nl2sql_runner<*>.ipynb from notebooks folder
2. Initialize the object like 
    ```code
    nl2sqlbq_client = Nl2sqlBq(project_id="vertexai-pgt",dataset_id="EY",metadata_json_path = "EY/metadata_cache.json",model_name="text-bison")
    ```
    Make sure you update the project id, dataset id and path to metadata_json

3. Save your question in a **question** variable and call generate sql like so

    ```code
    question = "your question here"
    gen_sql = nl2sqlbq_client.generate_sql(question)
    ```

    The above statement will generate SQL with zero-shot prompting.

    In you want to specify some examples (up to 3) for your question, ensure you have at least about 10 sample questions and corresponding SQLs are inserted in the PostgreSQL DB mentioned above.  Run

    ```code
    question = "your question here"
    gen_sql = nl2sqlbq_client.generate_sql_few_shot(question)
    ```

4. If you want to execute the query from the jupyter notebook then

    ```code
    result = nl2sqlbq_client.execute_query(sql_gen) # where sql_gen is the query generated by executing above steps
    ```


### Queries with JOIN

Generating SQL queries with JOIN is still a work-in-progress and not perfected yet.  Different approaches are being worked on to generate SQL queries with JOINs.  Separate prompts are developed for Join.  Prompts can be zero-shot or one-shot

The approaches are

1. STANDARD - No change related to how normal queries are generated, but two table names should be specified
2. MULTI_TURN - Same prompt to identify tables using table_filter_prompt as earlier, but a follow-up prompt is included to direct the LLM to identify another table for JOIN.  
3. SELF_CORRECT - Same as standard, but the approach tries to execute the SQL and repeats the SQL generation with the previously generated SQL as reference and improvise over it.  Max retries = 5

**generate_sql_with_join(<parameters>)** is the wrapper function for generating SQL with Joins.  This requires the following parameters

| Parameter   |      Description      |  Required/Optional |
|-------------|:---------------------:|-------------------:|
| data_set    |  BQ Dataset reference | Required |
| table_1_name | Name of the first table   |   Required |
| table_2_name | Name of second table |   Required |
| question     | NL question to which SQL to be generated |    Required |
| example_table1 | Table reference for one-shot |    Optional |
| example_table2 | Table reference for one-shot |    Optional |
| sample_question | Example question for on-shot |    Optional |
| sample_sql | Example SQL for one-shot|    Optional |
| one-shot | Boolean value True/False |    Default = False |
| join_gen | Approach to take. STANDARD, MULTI_TURN, SELF_CORRECT |    Default=STANDARD      |