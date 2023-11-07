import glob
import json
import random
# script names need to be standardized across downloaded configs
# remove support for patient sampling
def sample_url_config(models, script_names):

    url_config_files = glob.glob("url_configs/*.json")

    url_configs_model_filtered = []

    for model in models:
        url_configs_model_filtered.extend([file for file in url_config_files if model in file])

    url_configs_model_script_filtered = []

    for script in script_names:
        url_configs_model_script_filtered.extend([file for file in url_configs_model_filtered if script in file])

    # if patients.lower().strip() == "all":
    #     # unpack all the urls
    #     pass
    # else:
    #     # identify the url for the speciifc patient, should only be one script

    # unpack all the urls
    url_configs_to_sample = []
    for file in url_configs_model_script_filtered:
        with open(file) as f:
            data = json.load(f)
            url_configs_to_sample.extend(data)

    
    url_config = random.choice(url_configs_to_sample)
    return url_config
