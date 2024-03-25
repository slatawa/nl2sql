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

import vertexai
import re
import langchain
import pandas as pd
from tqdm import tqdm
import os

from text2sql_prediction.nl2sql import AskBQ
import re

PROJECT_ID = os.environ['PROJECT_ID']
REGION = os.environ['REGION']

TABLE_NAMES = ['medi-cal-and-calfresh-enrollment',
'calhhs-dashboard-2015-2020-annual-data-file',
'2019-2020-part-b-wic-redemptions-by-vendor-county-with-family-counts',
'wic-redemption-by-county-by-participant-category-data-2010-2018',
'calhhs-dashboard-2015-2020-annual-masking-key',
'calhhs-dashboard-2015-2020-july-data-file',
'calhhs-dashboard-2015-2020-july-masking-key',
'calhhs_ffs_provider_list',
'calhhs_medi-cal_managed_care_provider_listing']

def get_ask_obj(tbl_name):
  ask = AskBQ(
      location = os.environ['REGION'],
      project_id = os.environ['PROJECT_NUMBER'],
      dataset_id = os.environ['DATASET_ID'],
      enum_option_limit = 1000,
      result_row_limit = 1000,
      log_bucket="cdii-logger",
      table_names = [tbl_name],
      postprocessors=['case_handler_transform'],
      executor_chain = ['prompt_strategy', 'queryfix_strategy', 'agent_strategy'],
  )

  return ask

def get_correct_sql(sql):
  db_name = os.environ['DATASET_ID']
  tbl_names = re.findall(r'`(.*?)`', sql)
  for tbl_name in tbl_names:
    sql = sql.replace(tbl_name, '{}.{}'.format(db_name, tbl_name))
  return sql

def call_gen_sql(ask_objs, question):
  for obj in ask_objs:
    resp = obj(question)
    sql_out = resp.latest_sql
    if sql_out:
      return get_correct_sql(sql_out)
  return ''


def get_ask_bqs(tabl_names=TABLE_NAMES):
    ask_objs = [get_ask_obj(tbl) for tbl in tabl_names]

    return ask_objs

if __name__=='__main__':
    ask_objs = get_ask_bqs()
    sql = call_gen_sql(ask_objs, 'How many people are enrolled in CalFresh?')
