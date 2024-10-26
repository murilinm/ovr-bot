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
        del data[key_to_remove]
        with open(file_path,'w') as f:
            json.dump(data,f,indent=4, separators=(',', ': '))
        return print(f"Removed {key_to_remove} from {file_path}")
    else:
        return print(f"Error on deleting global variable key: {key_to_remove} from {file_path} does not exist.")