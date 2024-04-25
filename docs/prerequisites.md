# Pre-requisites -- this is linked from the main Readme.

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