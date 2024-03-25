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

import json
import pandas as pd

base_dir = '/Users/koushikchak/Downloads/fiserv/fiservsamplequeries/'
data_dict_file = 'Table List Documentation (1).xlsx'

table_file = 'Sample Report Data (1)/Funding_search.xlsx'
sheet_name = 'Funding'
table_name = 'Funding_search'


df_table = pd.read_excel(base_dir+table_file)
df_data_dict = pd.read_excel(base_dir+data_dict_file, sheet_name=sheet_name)

data_dict = {i: (j, k) for i, j, k in zip(df_data_dict.Name, df_data_dict.ID, df_data_dict.Description)}

final_dict = {}
for col in df_table.columns:
    if col in data_dict:
        key = table_name + '.' + data_dict[col][0]
        value = data_dict[col][1]
        final_dict[key] = value
    else:
        print(col)


with open(base_dir+table_name+'.json', 'w') as f:
    json.dump(final_dict, f, indent=4)
