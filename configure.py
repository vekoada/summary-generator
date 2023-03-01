import json

def get_credentials(path):
    with open(path) as f:
        return json.load(f)