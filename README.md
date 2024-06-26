# NL2SQL Generic Library

## Pre-requisites

### PostgreSQL DB
Create a PostGreSQL instance and DB in Cloud SQL

On Google Cloud Console -

    Go to Cloud SQL
    Click Create Instance
    Select PostGreSQL
    Specify the instance name and Password.  Note: username is default postgres

    Once the instance is created,
        Click on the instance
        Click Databases
        Click Create Database 
    
    Note the PostgreSQL Instance ID, DB and Password and specify in the environment variables mentioned below
    
### Dataset in BQ
Create the Dataset and import the tables and data into BQ


### Creating Metadata Cache file for your BQ dataset

SQL Generation is dependent on the LLM knowing the tables and columns that are to be considered for generating the SQL.  The BQ dataset, tables and columns are different for each client requirement.  Description of the table and the columns in the table are required to be provided to the LLM for SQL query generation

This data of tables, columns and their description are provided in JSON format in a file named **metadata_cache.json**.  This file is in the nl2sql_src/cache_metadata folder.

In order to generate the metadata_cache.json for your project, 

1. Open metadata_update_bq.py
2. Update the *PROJECT_ID*  *DATASET* fields
3. Go to nl2sql_generic/nl2sql_src folder
4. Set the python environment and run 

    ```code
    python metadata_update_bq.py
    ```


### Environment Variables
```bash
PROJECT_ID='sl-test-project' # Update for your project
REGION='us-central1'
DATASET_NAME='sl-test-project.EY' # Update for your project
DATASET_ID='EY' # Update for your project
PROJECT_NUMBER='sl-test-project' # Update for your project
PG_INSTANCE='test-nl2sql' # Update for your project
PG_DB='test-db' # Update for your project
PG_USER='postgres'
PG_PWD='test-nl2sql' # Update for your project
```

## Modules and Descriptions

### nl2sql_src

nl2sql_src is the generic library for generating SQL. 

#### Files

**nl2sql_generic.py** is the main file with **Nl2sqlBq** as the main class used for generating SQL
**nl2sql_query_embeddings.py** is used for creating embeddings for sample questions to be used as examples
**Prompts.py** contains all the prompts used for identifying tables, generating SQL etc.,
**metadata_update_bq.py** used to created the metadata_cache.json from BQ dataset


### Notebooks
1. Modify the nl2sql_runner_*.ipynb parameters to access the required resources on the project to generate the SQL
2. nl2sql_vectordb_search.ipynb notebook can be used to create PostgreSQL table, insert records and retrieve closest matching queries.  Please ensure PostGreSQL instance and Database are already creted from console
3. Others notebooks can be used for experienting and evaluating query generation

### py-backend-api
py-backend-api consists of backend services which are created using Python Flask library. This module converts the requests to generated SQL into backend apis. 

**app.py** is the entry point.

### WebApp

webapp consists of Web application related resources.  API endpoints are mentioned in the .env.development, .env.production for development and production deployment respectively

**Note** : Do not change the key names in the .env.* files. Only update the values (mostly app engine endpoints of backend deployment)




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