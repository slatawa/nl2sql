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

import pandas
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel
import os

DATASET_NAME = os.environ["DATASET_NAME"]
model_geminipro = GenerativeModel("gemini-pro")
parameters_geminipro = GenerationConfig(
                temperature=0,
                top_p=0,
                top_k=1
                # candidate_count=1,
                # max_output_tokens=512,
                # stop_sequences=["STOP!"],
            )

def generate_geminipro(prompt, parameters_geminipro):
    # prompt is the instruction for the model
    response = model_geminipro.generate_content(prompt)
    return response.text

def generate_sql_geminipro(query_description, parameters):
    # takes in some parameters describing a table and a user request, and uses PALM to generate an SQL statement
    prompt= open('./nl2sql_textbison_geminipro/prompt.txt').read()
    result = generate_geminipro(prompt.format(DATASET_NAME=DATASET_NAME,question=query_description), parameters_geminipro)
    if result == 'No Response':
      return
    return result
