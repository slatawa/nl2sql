from nl2sql_src.nl2sql_generic import Nl2sqlBq


# Initializing 1st time for a dataset
nl2sqlbq_client = Nl2sqlBq(project_id="sl-test-project-353312", dataset_id="EY")

# When Initializing for first time , you will need to create metadata_json
nl2sqlbq_client.create_metadata_json(metadata_json_dest_path="EY/metadata_cache.json",
                                     data_dict_path="EY/data_dictionary.json",
                                     col_values_distribution=True)

# Initializing when metadata cache is already created
nl2sqlbq_client = Nl2sqlBq(project_id="sl-test-project-353312", dataset_id="EY",
                           metadata_json_path="EY/metadata_cache.json", model_name="text-bison")

question = "What projects are impacting my engagement code E-67747458?"

# Convert to sql
query = nl2sqlbq_client.generate_sql(question)
print(query)
