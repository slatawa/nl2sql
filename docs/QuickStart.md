# Quick Start Guide
<div style="text-align: right">

[Back](README.md)
</div>

## Cloning the NL2SQL Generic Library Repository

Clone the repository using the commands below
 
    git clone git@github.com:slatawa/nl2sql-generic.git

    cd nl2sql_generic
 

___

## Setup 

Creating PostgreSQL tables and adding examples to dataset

1. Open nl2sql_vectordb_search.ipynb notebook

2. Update the following variables in the notebook

    ```PGPROJ = "sl-test--project"
    PGLOCATION = 'us-central1'
    PGINSTANCE = "test-nl2sql"
    PGDB = "test-db"
    PGUSER = "postgres"
    PGPWD = "test-nl2sql"
    ```
3. Execute the cells in the notebook 

___

## Creating the metadata_cache.json

1. Change to nl2sql_src folder

    ```code
    cd nl2sql_src
    ```
2. Update environment variables

    ```
    PROJECT_ID - [example : sl-test-project]
    DATASET_NAME - [example : sl-test-project.zoominfo]
    ```

3. Execute the metadata_update_bq file

    ```code
    python metadata_update_bq.py
    ```
4. Verify the generated **metadata_cache.json** file created in **cache_metadata** folder

___

## Generating SQL

1. Open the notebook nl2slql_runner.ipynb

2. Change the **PROJECT_ID** and **DATASET_ID** according to your project

3. Update the question

4. Execute the cells and observe the output


