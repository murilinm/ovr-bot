import json

def update_json_file(file_path: str, new_data):
    with open(file_path, "r") as file:
        data = json.load(file)

    data.update(new_data)
    
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, separators=(',', ': '))
    
    print(f"Updated {file_path} with: {new_data}")

def delete_key(file_path: str, key_to_remove: str):
    with open(file_path, "r") as file:
        data = json.load(file)
        
    key_to_remove = str(key_to_remove)
    
    if key_to_remove in data:
        key_data = data[key_to_remove]
        del data[key_to_remove]
        with open(file_path,'w') as f:
            json.dump(data,f,indent=4, separators=(',', ': '))
        return print(f"Removed {key_to_remove} ({key_data}) from {file_path}")
    else:
        return print(f"Error on deleting global variable key: {key_to_remove} from {file_path} does not exist.")
    
def update_specific_data(fp: str, new_data, key1: str, key2: str):
    with open(fp, "r") as f:
        data = json.load(f)
    data[str(key1)][str(key2)]=new_data
    with open(fp, "w") as f:
        json.dump(data, f, indent=4, separators=(',', ': '))
    print(f"Updated {key2} from {key1} ({fp}) with {new_data}")