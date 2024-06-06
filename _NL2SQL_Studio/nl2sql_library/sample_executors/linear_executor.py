"""
    SQL Generation using Linear Executor
"""
import json
# import os
import sys
from os.path import dirname, abspath
from loguru import logger

sys.path.insert(1, dirname(dirname(abspath(__file__))))

# from nl2sql.datasets.base import Dataset
from nl2sql.executors.linear_executor.core import CoreLinearExecutor

dataset_name ="zoominfo" # @param {type:"string"}
metadata_cache_file = open('../utils/zoominfo_tables.json', encoding="utf-8")
zoominfo_data = json.load(metadata_cache_file)

data_dictionary_read = {
            "zoominfo": {
                "description" : "This dataset contains information of Zoominfo Data\
                  with details on headquarters, marketing professionaals and\
                    providng tuition services.",
                "tables": 
                   zoominfo_data
            },
    }


## Executor Setup Code

bigquery_connection_string = "bigquery://sl-test-project-363109/zoominfo" # @param {type:"string"}

executor = CoreLinearExecutor.from_connection_string_map(
   {
       dataset_name: bigquery_connection_string,
   },
   data_dictionary = data_dictionary_read
)

logger.info(f"Executor ID : {executor.executor_id}")

## Now run the executor with a sample question
result = executor(
   db_name= dataset_name,
   question = "What is the revenue of construction industry?" # @param {type:"string"}
)
logger.info(f"Result ID : {result.result_id}")
logger.info(f"Generated SQL : \n {result.generated_query}")
