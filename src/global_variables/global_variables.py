import json
import logging
import os

# FUNCTIONS
def log_to_file(fp, message):
    log_file = os.path.join(os.path.dirname(__file__), '..', 'ovr-bot.log')
    
    if log_file:
        with open(log_file, "a") as f:
            logging.info(message)
    else:
        logging.error(f'logs/log.py function received invalid file path: {fp}')

# CODE
def update_json_file(file_path: str, new_data):
    with open(file_path, "r") as file:
        data = json.load(file)

    data.update(new_data)
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, separators=(',', ': '))
    
    print(f"Updated {file_path} with: {new_data}")
    #log.new_object(fp=file_path, new_data=new_data)
    log_to_file(file_path, f"NEW OBJECT ON {file_path}: DATA {new_data}")

def delete_key(file_path: str, key_to_remove: str):
    with open(file_path, "r") as file:
        data = json.load(file)
        
    key_to_remove = str(key_to_remove)
    
    if key_to_remove in data:
        key_data = data[key_to_remove]
        del data[key_to_remove]
        with open(file_path,'w') as f:
            json.dump(data,f,indent=4, separators=(',', ': '))
            #log.object_deleted(file_path=file_path, key=key_to_remove, key_data=key_data)

        log_to_file(file_path, f"OBJECT DELETED ON {file_path}: KEY {key_to_remove}; DATA: {key_data}")
        return print(f"Removed {key_to_remove} ({key_data}) from {file_path}")
    else:
        return print(f"Error on deleting global variable key: {key_to_remove} from {file_path} does not exist.")


def update_specific_data(fp: str, new_data, key1: str, key2: str):
    with open(fp, "r") as f:
        data = json.load(f)
    old = data[str(key1)][str(key2)]
    data[str(key1)][str(key2)]=new_data
    with open(fp, "w") as f:
        json.dump(data, f, indent=4, separators=(',', ': '))
    print(f"Updated {key2} from {key1} ({fp}) with {new_data}")
    log_to_file(fp, f"OBJECT UPDATED ON {fp}: KEY {key1}; OLD DATA: '{old}'; NEW DATA: {new_data}")