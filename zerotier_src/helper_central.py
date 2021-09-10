import requests
import json

debug = False

def get_network(central_token):
    headers = {
        "Authorization":f"Bearer {central_token}",
        "Content-Type":"application/json"
    }
    r = requests.get("https://my.zerotier.com/api/v1/network",headers=headers)
    if debug:
        print(r.json())
    return r.json()

def create_network(central_token):
    headers = {
        "Authorization":f"Bearer {central_token}",
        "Content-Type":"application/json"
    }
    
    r = requests.post("https://my.zerotier.com/api/v1/network",headers=headers,data="{}")
    if debug:
        print(r.json())
    return r.json()

def assign_network_name(central_token,network_id,name):
    headers = {
        "Authorization":f"Bearer {central_token}",
        "Content-Type":"application/json"
    }
    body = {
        "config": {
            "name": name
        }
    }
    body = json.dumps(body)
    r = requests.post(f"https://my.zerotier.com/api/v1/network/{network_id}",headers=headers,data=body)
    if debug:
        print(r)
        print(r.json())
    return r.json()

def modify_route(central_token,network_id,routes):
    headers = {
        "Authorization":f"Bearer {central_token}",
        "Content-Type":"application/json"
    }
    body = {
        "config": {
            "routes":routes
        }
    }
    body = json.dumps(body).replace("\"null\"","null") #Ensuring format due to Zerotier API requirement
    r = requests.post(f"https://my.zerotier.com/api/v1/network/{network_id}",headers=headers,data=body)
    if debug:
        print(r)
        print(r.json())
    return r.json()

def delete_member(central_token,network_id,member_id):
    headers = {
        "Authorization":f"Bearer {central_token}",
        "Content-Type":"application/json"
    }
    r = requests.delete(f"https://my.zerotier.com/api/v1/network/{network_id}/member/{member_id}",headers=headers)
    if debug:    
        print(r)

def assign_member_ip(central_token,network_id,member_id,ip_address):
    headers = {
        "Authorization":f"Bearer {central_token}",
        "Content-Type":"application/json"
    }
    body = {
        "config": {
            "ipAssignments": [
                ip_address
            ]
        }
    }
    body = json.dumps(body)
    r = requests.post(f"https://my.zerotier.com/api/v1/network/{network_id}/member/{member_id}",headers=headers,data=body)
    if debug:
        print(r)
        print(r.json())
    return r.json()

def assign_member_name_desc(central_token,network_id,member_id,name,desc):
    headers = {
        "Authorization":f"Bearer {central_token}",
        "Content-Type":"application/json"
    }
    body = {
        "name":name,
        "description":desc
    }
    body = json.dumps(body)
    r = requests.post(f"https://my.zerotier.com/api/v1/network/{network_id}/member/{member_id}",headers=headers,data=body)
    if debug:
        print(r)
        print(r.json())
    return r.json()