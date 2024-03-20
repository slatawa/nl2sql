SQL_GEN_PROMPTS = [
    '''Only use the following tables meta-data:

```
{metadata_json[tables_list[0]]}
```

You are an SQL expert at generating SQL queries from a natural language question. Given the input question, create a syntactically correct BigQuery query to run.

Only use the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Do not use more than 10 columns in the query. Focus on the keywords indicating calculation. 
Please think step by step and always validate the reponse.
recitify each column names by referencing them from the meta-data.

For this question what would be the most accurate SQL query?
Question: {question}''',

    '''Only use the following tables meta-data:

```
{metadata_json[tables_list[0]]}
```

You are an SQL expert at generating SQL queries from a natural language question. Given the input question, create a syntactically correct BigQuery query to run.

Only use the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Do not use more than 10 columns in the query. Focus on the keywords indicating calculation. 
Please think step by step and always validate the reponse.
recitify each column names by referencing them from the meta-data.

NOTE: Take a deep breath and double check all syntax are compatible with with BIGQUERY.

For this question what would be the most accurate SQL query?
Question: {question}''',

    '''Only use the following tables meta-data:

```
{metadata_json[tables_list[0]]}
```

You are an SQL expert at generating SQL queries from a natural language question. Given the input question, create a syntactically correct BigQuery query to run.

Only use the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Do not use more than 10 columns in the query. Focus on the keywords indicating calculation. 
Please think step by step and always validate the reponse.
recitify each column names by referencing them from the meta-data.

NOTE: Make sure all syntax are compatible with with BIGQUERY.

For this question what would be the most accurate SQL query?
Question: {question}''',

    '''Only use the following tables meta-data:

```
{metadata_json[tables_list[0]]}
```

You are an SQL expert at generating SQL queries from a natural language question. Given the input question, create a syntactically correct BigQuery query to run.

Only use the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Do not use more than 10 columns in the query. Focus on the keywords indicating calculation. 
Please think step by step and always validate the reponse.
recitify each column names by referencing them from the meta-data.

NOTE: Make sure all syntax are compatible with with BIGQUERY.
Cast DATETIME to STRING before applying SUBSTR on DATETIME columns.

For this question what would be the most accurate SQL query?
Question: {question}'''
]


TABLE_FILTER_PROMPTS = [
'''You are a database expert at selecting a table from a list of tables based on their description.
    For the provided question choose what is the table_name most likely to be relevant.
    Only mention the table name from the following list and their description-keywords. Mention multiple tables names if applicable.

    Table name | description-keywords
    authorizations_search | This table contains information about all the transactions in sales and their details like status, date, network, payment methods etc. Auth, Sale, Flow, Transaction
    settlement_search | The Approved Transactions are now sent for Settlement. Settlement transactions are the first step in Funding the merchant. Keywords are Settled, Settlement, Settle
    chargebacks_search | Chargebacks Search Table, Dispute, Chargeback
    funding_search | Fund, Deposit
    
    Question: {question}
    ''',

'''You are a database expert at selecting a table from a list of tables based on their description.
    For the provided question choose what is the table_name most likely to be relevant.
    Only select the table from the following list and their description-keywords. Select multiple tables if applicable.

    Table name | description-keywords
    authorizations_search | This table contains information about all the transactions in sales and their details like status, date, network, payment methods etc. Auth, Sale, Flow, Transaction
    settlement_search | The Approved Transactions are now sent for Settlement. Settlement transactions are the first step in Funding the merchant. Keywords are Settled, Settlement, Settle
    chargebacks_search | Chargebacks Search Table, Dispute, Chargeback
    funding_search | Fund, Deposit
    
    Question: {question}
    '''
]

NL_EXPLAIN_PROMPTS = [
'''You are an expert Data Analyst. Given a report of SQL query and the question in
        natural language, provide a very insightful, intuitive and a not too long well-explained summary of the
        result which would help the user understand the result better and take informed decisions. 
        If the result does not have any data, then just mention that briefly in the summary.
        question: {question}
        result: {str(result)}''',

'''You are an expert Data Analyst. Given a report of SQL query and the question in
        natural language, provide a very crisp, short, intuitive and easy-to-understand summary of the result.
        If the result does not have any data, then just mention that briefly in the summary.
        question: {question}
        result: {str(result)}'''
]

SQL_CORRECTION_PROMPTS = [
'''You are an SQL expert at correcting SQL queries so that it is completely compatible 
    with BigQuery and syntactically correct. If nothing needs to be changed then just give the query as it is.
    If some functions are not present in buigquery then
    replace them with functions which can be run in BigQuery.
    Also Cast DATETIME to STRING before applying SUBSTR or any other string manipulation functions on DATETIME columns when needed.

    For this sql what is the BigQuery compatible query?
    SQL: {sql}''',

]

AUTO_VERIFY_PROMPTS = [
'''You are an expert at validating SQL queries. Given the Natrual language description
      and the SQL query corresponding to that description, please check if the students answer is correct.
      There can be different ways to achieve the same result by forming the query differently.
      If the students SQL query matches the ground truth and fits the NL description correctly, then return yes
      else return no.
      Natural language description: {nl_description}
      Ground truth: {ground_truth}
      students answer: {llm_amswer}
    ''',
]