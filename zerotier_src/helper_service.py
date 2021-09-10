import requests
import json

debug = False

def get_node_id(service_token):
    headers = {
        "X-ZT1-Auth":service_token,
        "Content-Type":"application/json"
    }
    r = requests.get("http://localhost:9993/status",headers=headers)
    return r.json()["address"]

def join_network(service_token,network_id):
    headers = {
        "X-ZT1-Auth":service_token,
        "Content-Type":"application/json"
    }
    
    r = requests.post(f"http://localhost:9993/network/{network_id}",headers=headers,data="{}")
    if debug:
        print(r)
        print(r.json())
    return r.json()