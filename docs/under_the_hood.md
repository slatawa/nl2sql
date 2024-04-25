# Under the hood - design and architecture
<div style="text-align: right">

[Back](README.md)
</div>

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

