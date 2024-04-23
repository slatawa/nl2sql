# NL2SQL Generic Library

## Pre-requisites

### PostgreSQL DB

### Dataset in BQ


### Environment Variables
PROJECT_ID='sl-test-project' # Update for your project
REGION='us-central1'
DATASET_NAME='sl-test-project.EY' # Update for your project
DATASET_ID='EY' # Update for your project
PROJECT_NUMBER='sl-test-project' # Update for your project
PG_INSTANCE='test-nl2sql' # Update for your project
PG_DB='test-db' # Update for your project
PG_USER='postgres'
PG_PWD='test-nl2sql' # Update for your project

## Modules and Descriptions

### nl2sql_src

nl2sql_src is the generic library for generating SQL. 

#### Files

**nl2sql_generic.py** is the main file with **Nl2sqlBq** as the main class used for generating SQL
**nl2sql_query_embeddings.py** is used for creating embeddings for sample questions to be used as examples
**Prompts.py** contains all the prompts used for identifying tables, generating SQL etc
**metadata_update_bq.py** used to created the metadata_cache.json from BQ dataset


### Notebooks
1. Modify the nl2sql_runner_*.ipynb parameters to access the required resources on the project to generate the SQL
2. nl2sql_vectordb_search.ipynb notebook can be used to create PostgreSQL table, insert records and retrieve closest matching queries.  Please ensure PostGreSQL instance and Database are already creted from console
3. Others notebooks can be used for experienting and evaluating query generation

### py-backend-api


### WebApp




## Starting Front-end and Back-end modules

### Launching the back-end locally

### Launching the front-end locally

## Deploying the Application on App Engine

### Deploying Back-end service

### Deploying Front-end service

## API Integration
