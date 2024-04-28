# Multi-turn SQL Generation
<div style="text-align: right">

[Back](README.md)
</div>

Many a times there are questions that build over the previous question or a variation of the same.  Most of the context for the question is the same.  Without the original question the is minimal information for the LLM to deduce the input and generate the SQL.

Using Multi-turn chat based execution, the original question and follow-up questions can be executed without the need to specify the context for every question.  

The context from the first question is used to respond with SQL queries for subsequent questions

## Generating questions using Multi-turn

1. Open the nl2sql_multi-turn.ipynb notebook

2. Update the project details

    ```
    PROJECT_ID
    DATASET_ID
    ```
3. Specify the original (base) question and the follow-up questions in the **questions** array.  Make sure the base question is the first element of the array

4. Execute the cells in the notebook to generate the SQL for each question in the array.  

You can view the original context and the LLM responses in the chat history using

```    
sql_chat.history
```