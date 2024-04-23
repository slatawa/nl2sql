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

app.py is the entry point.

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

url = <your api endpoint url>
data = {"question": question, "unique_id":uniqueid}
headers={"Content-type":"application/json", "Accept":"text/plan"}
resp = requests.post(url_sql_gen, data=json.dumps(data), headers=headers)

resp = requests.get(url_display)
print('Generated SQL - ', resp[0]['sql])

```

## Using Webapp interface

1. Launch the Web interface (either locally or in App engine - see above)
2. Type your question in the Question input field and click Submit
3. Generated SQL will be displayed below the question input field

## Using Jupyter notebook

## 
