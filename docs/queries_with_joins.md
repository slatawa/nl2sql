# Generating SQL queries with JOINs
<div style="text-align: right">

[Back](README.md)
</div>

Generating SQL queries with JOIN is still a work-in-progress.  Different approaches are being worked on to generate SQL queries with JOINs.  Separate prompts are developed for Join.  Prompts can be zero-shot or one-shot

The approaches are

1. **STANDARD** - No change related to how normal queries are generated, but two table names should be specified

2. **MULTI_TURN** - Same prompt to identify tables using table_filter_prompt as earlier, but a follow-up prompt is included to direct the LLM to identify another table for JOIN.

3. **SELF_CORRECT** - Same as standard, but the approach tries to execute the SQL and repeats the SQL generation with the previously generated SQL as reference and improvise over it.  Max retries = 5


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

## Generating SQL queries with JOIN

1. Open the nl2sql_sql_with_joins.ipynb notebook

2. Update the following variables

    ```
    PROJECT_ID
    DATASET_ID
    ```
3. Update the variables to specify the examples (NL statement, SQL with join, Tables) in the notebook 

3. Run the cells in the notebook to verify SQL with Join generation