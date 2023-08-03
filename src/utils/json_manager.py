import json
import os

def read_json(path:str)-> list:
    if not os.path.isfile(path):
        with open(path, "w") as f:
            json.dump([], f)
    
    with open(path, "r") as f:
        data = json.load(f)
        
    return data
        

def write_json(path:str, data:list)-> list:
    with open(path, "w") as f:
        json.dump(data,f)