Table_filtering_prompt = """
You are a database expert at selecting a table from a list of tables based on their description.
For the provided question choose what is the table_name most likely to be relevant.
Only mention the table name from the following list and their description.
Do not mention any information more than the table name.
Output should be only 1 table that is the most likely table to contain the relevant data
Do not include any special characters in the generated output

Table name | description
{only_tables_info}

Question: {question}
"""

Table_filtering_prompt_promptonly = """
You are a database expert at selecting a table from a list of tables based on their description.
For the provided question choose what is the table_name most likely to be relevant.
Only mention the table name from the following list and their description.
Do not mention any information more than the table name.
Output should be only 1 table that is the most likely table to contain the relevant data
Do not include any special characters in the generated output

Table name | description
{only_tables_info}

"""

Result2nl_insight_prompt = '''
You are an expert Data Analyst. Given a report of SQL query and the question in
natural language, provide a very insightful, intuitive and a not too long well-explained summary of the
result which would help the user understand the result better and take informed decisions. 
If the result does not have any data, then just mention that briefly in the summary.
question: {question}
result: {result}'''

Result2nl_prompt = '''
You are an expert Data Analyst. Given a report of SQL query and the question in
natural language, provide a very crisp, short, intuitive and easy-to-understand summary of the result.
If the result does not have any data, then just mention that briefly in the summary.
question: {question}
result: {result}
'''

Auto_verify_sql_prompt = '''
You are an expert at validating SQL queries. Given the Natrual language description
and the SQL query corresponding to that description, please check if the students answer is correct.
There can be different ways to achieve the same result by forming the query differently.
If the students SQL query matches the ground truth and fits the NL description correctly, then return yes
else return no.
Natural language description: {nl_description}
Ground truth: {ground_truth}
students answer: {llm_amswer}
'''



Sql_Generation_prompt = '''
Only use the following tables meta-data:

```
Table Name : {table_name}

Description: {table_description}

This table has the following columns : 
{columns_info}
\n
```

You are an SQL expert at generating SQL queries from a natural language question. Given the input question, create a syntactically correct Biguery query to run.

Only use the few relevant columns given the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Do not use more than 10 columns in the query. Focus on the keywords indicating calculation. 
Please think step by step and always validate the reponse.
recitify each column names by referencing them from the meta-data.

For this question what would be the most accurate SQL query?
Question: {question}
'''

Sql_Generation_prompt_few_shot = '''
Only use the following tables meta-data:

```
Table Name : {table_name}

Description: {table_description}

This table has the following columns : 
{columns_info}
\n
```

You are an SQL expert at generating SQL queries from a natural language question. Given the input question, create a syntactically correct Biguery query to run.

Only use the few relevant columns given in the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Do not use more than 10 columns in the query. Focus on the keywords indicating calculation. 
Please think step by step and always validate the reponse.
recitify each column names by referencing them from the meta-data.
Use the following examples as guidelines to generate the new BigQuery SQL accordingly

{few_shot_examples}

For this question what would be the most accurate SQL query?
Question: {question}
'''

Sql_Generation_prompt_few_shot_multiturn = '''
Only use the following tables meta-data:

```
Table Name : {table_name}

Description: {table_description}

This table has the following columns : 
{columns_info}
\n
```

You are an SQL expert at generating SQL queries from a natural language question. Given the input question, create a syntactically correct Biguery query to run.

Only use the few relevant columns given in the question.
Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Do not use more than 10 columns in the query. Focus on the keywords indicating calculation. 
Please think step by step and always validate the reponse.
recitify each column names by referencing them from the meta-data.
Use the following examples as guidelines to generate the new BigQuery SQL accordingly

{few_shot_examples}

{additional_context}

For this question what would be the most accurate SQL query?
Question: {question}
'''

additional_context_prompt = """You are database expert who can generate SQL query statements for data analysis.
SQL query for a prior question is given below
{prev_sql}
Enhance this SQL query to fulfil the requirements of the question given below
"""
