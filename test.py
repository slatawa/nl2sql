import configparser
from nl2sql_src.nl2sql_generic import Nl2sqlBq

config_file = 'config.ini'
config_version = 'default'
config = configparser.ConfigParser()
config.read(config_file)

options = config.options(config_version)
project_id = config.get(config_version, "project_id")
dataset_id = config.get(config_version, "dataset_id")
metadata_json_dest_path = config.get(config_version, "metadata_json_dest_path")
if "data_dict_path" in options:
    data_dict_path = config.get(config_version, "data_dict_path")
else:
    data_dict_path = None
metadata_already_created = config.get(config_version, "metadata_already_created")

#print(project_id,dataset_id,metadata_json_dest_path,data_dict_path,metadata_already_created)


if not int(metadata_already_created):
    # Initializing 1st time for a dataset
    nl2sqlbq_client = Nl2sqlBq(project_id=project_id, dataset_id=dataset_id)

    # When Initializing for first time , you will need to create metadata_json
    nl2sqlbq_client.create_metadata_json(metadata_json_dest_path=metadata_json_dest_path,
                                         data_dict_path=data_dict_path,
                                         col_values_distribution=True)
else:
    # Initializing when metadata cache is already created
    nl2sqlbq_client = Nl2sqlBq(project_id=project_id, dataset_id=dataset_id,
                               metadata_json_path=metadata_json_dest_path, model_name="text-bison")

question = "What projects are impacting my engagement code E-67747458?"

# Convert to sql
query = nl2sqlbq_client.generate_sql(question)
print(query)
