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

from vertexai.preview.language_models import TextGenerationModel
import os

DATASET_NAME = DATASET_NAME = os.environ["DATASET_NAME"]
model_textbison1 = TextGenerationModel.from_pretrained("text-bison-32k@002")
parameters_textbison1 = {
    "temperature": 0,
    "max_output_tokens": 8192,
    "top_p": 0,
    "top_k": 1,
}


def generate_textbison1(prompt, parameters):
    # prompt is the instruction for the model
    response = model_textbison1.predict(prompt, **parameters_textbison1)
    return response.text


def generate_sql_textbison1(query_description, parameters):
    prompt = open('./nl2sql_textbison_geminipro/prompt.txt').read()
    result = generate_textbison1(prompt.format(
        DATASET_NAME=DATASET_NAME, question=query_description), parameters_textbison1)
    if result == 'No Response':
        return
    print(result)
    return result
