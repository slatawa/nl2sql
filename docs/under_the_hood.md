# Under the hood - Module organisation
<div style="text-align: right">

[Back](README.md)
</div>

## Modules and Descriptions

### Folder structure

Important folders and files in the library are shown in the structure below.  
```
./nl2sql_generic
├── nl2sql_src
  └── __init__.py
  └── nl2sql_generic.py
  └── metadata_update_bq.py
  └── nl2sql_query_embeddings.py
  └── prompts.py
  └── test.py
  └── cache_metadata
    └── metadata_cache.json
    └── saved_index_pgdata
  └── data_dict
    └── data_dictionary.json
  └── dataset
  └── output
  └── utils
    └── mmake_data_dict.py
    └── table_filter_test.py
└── notebooks
  └── nl2sql_runner.ipynb
  └── nl2sql_vectordb_search.ipynb
  └── nl2sql_multi-turn.ipynb
  └── nl2sql_sql_with_joins.ipynb
  └── <other temp notebooks>
└── py-backend-api
  └── app.py
  └── app.yaml
  └── requirements.txt
  └── <other temp files>
└── webapp*
  └── src*
    └── components
        └── resultsInsights
            └── HistoricalData.tsx
            └── InfoModal.tsx
            └── ResultData.tsx
            └── ResultDataDisplay.tsx
  └── functions
  └── scripts
  └── app.yaml
  └── .env.development
  └── .env.production
  └── package.json
  └── index.html
  └── Dockerfile
  └── vite config.ts

```
There are several other folders in the file organisation that is not depicted above 


### nl2sql_src

nl2sql_src is the generic library for generating SQL. 

#### Files

* **nl2sql_generic.py** is the main file with **NL2sqlBq** as the main class for generating SQL

* **nl2sql_query_embeddings.py** is used for creating embeddings for sample questions to be used as examples

* **Prompts.py** contains all the prompts used for identifying tables, generating SQL etc.,

* **metadata_update_bq.py** used to create the metadata_cache.json from BQ dataset


### Notebooks
1. Modify the **nl2sql_runner.ipynb** parameters to access the required resources on the project to generate the SQL

2. **nl2sql_vectordb_search.ipynb** notebook can be used to create PostgreSQL table, insert records and retrieve closest matching queries.  Please ensure PostGreSQL instance and Database are already creted from console

3. **nl2sql_multi-turn.ipynb** notebook allows generation of SQL for a series of questions as follow-up question of base question

4. **nl2sql_sql_with_joins.ipynb** can be used for generating SQLs with Join using three different approaches - STANDARD, MULTI_TURN and SELF-CORRECT

5. Others notebooks can be used for experienting and evaluating query generation


### py-backend-api

py-backend-api consists of backend services which are created using Python Flask library. This module contains the functions to convert the requests into generated SQL and exposes the functions as backend APIs. 

**app.py** is the entry point for this module


### WebApp

**webapp** consists of Web application related resources.  API endpoints are mentioned in the .env.development, .env.production for development and production deployment respectively

At present, the UI module supports only 2 APIs **/api/sqlgen** and **/api/display**

**Note** : Do not change the key names in the .env.* files. Only update the values (mostly app engine endpoints of backend deployment)

