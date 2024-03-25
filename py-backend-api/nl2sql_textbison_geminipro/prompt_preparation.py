# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import re

tabl2query = 'Another example, to {question}, the bigquery sql string is  {sql_string}'
table_desc = 'The table has the following columns {columns}. The table name is {table_name}.'

mod_prompt = '''
You are a helpful assistant that can generate SQL queries for a bigquery table, given a list of columns in a table and a description of the users intent.
For example, to find how many people are enrolled in CalFresh, the bigquery sql string is  SELECT COALESCE(SUM(SAFE_CAST( Person AS INT64)), 0) AS total_beneficiaries FROM `cdii-poc.HHS_Program_Counts.calhhs-dashboard-2015-2020-annual-data-file` where Program = 'CalFresh';.
{tabl2query}
Your answer should only contain the sql string without any backticks etc
=========
{table_desc}
==========
Basis the knowledge above generate a sql query which should be used to generate response from biquery database. The query should extract relevant results of {question}

Output Structure:
1. Basis the knowledge above generate a sql query which should be used to generate response from biquery database
2. Your answer should only contain the sql string without any backticks etc
3. If you are not able to answer the query basis the knowledge, return response as string 'No Response'
'''

def get_prompt(sdf):
    tables_list = []
    sql_query = """
        SELECT * FROM `{table_name}` LIMIT 100
    """
    table_desc_concat = ''
    table2query_concat = ''

    for question, sql in zip(sdf.questions.values, sdf.sql.values):
        tablename = re.findall(r'`(.*?)`', sql)[0]
        if tablename not in tables_list:
            tables_list.append(tablename)
            df = pd.read_gbq(sql_query.format(table_name=tablename), dialect='standard')
            print(df)
            columns = list(df.columns)
            if table_desc_concat:
                table_desc_concat += '\n'
            table_desc_concat += table_desc.format(columns=columns, table_name=tablename)
        if table2query_concat:
            table2query_concat += '\n' 
        table2query_concat += tabl2query.format(question=question, sql_string=sql)

    return mod_prompt.format(tabl2query=table2query_concat,
                  table_desc=table_desc_concat, question='{question}')

if __name__=='__main__':
    df = pd.read_csv('question_query_map.csv')
    prompt = get_prompt(df)
    with open('./prompt.txt', 'w') as f:
        f.write(prompt)
