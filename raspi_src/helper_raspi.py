import re
import requests
import json

debug = False

def enable_uart_config(config_file_list):
    #Input is a list of strings
    enable_uart_pattern = re.compile(r'enable_uart=*')
    enable_uart_index = -1
    for index,line in enumerate(config_file_list):
        if (enable_uart_pattern.match(line)):
            #print("Found!")
            #print(f"Index: {index}")
            #print(f"Line: {line}")
            enable_uart_index = index
        else:
            #print("Not found.")
            pass

    if (enable_uart_index != -1):
        config_file_list[enable_uart_index] = "enable_uart=1\n"
    else:
        config_file_list.append("enable_uart=1\n")

    return config_file_list


def enable_wifi_config(country,ssid,password):
    wifi_config_list = [
        f"country={country}\n",
        "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n",
        "update_config=1\n",
        "\n",
        "network={\n",
        f"ssid=\"{ssid}\"\n",
        "scan_ssid=1\n",
        f"psk=\"{password}\"\n",
        "key_mgmt=WPA-PSK\n",
        "}\n"
    ]

    return wifi_config_list


def read_buffer(stdout):
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line, end="")


def execute_single_command(command, client):
    print(f"Executing command: {command}")
     # Run a command (execute ping)
    stdin, stdout, stderr = client.exec_command(command)

    # Print output line by line.
    read_buffer(stdout)

    #Script return code
    print()
    print(f'Return code: {stdout.channel.recv_exit_status()}')

    #Close the channel
    stdin.close()
    stdout.close()
    stderr.close()

    if (int(stdout.channel.recv_exit_status()) != 0):
        raise Exception(f"Unsuccessful command execution. Command: {command}")

def get_zerotier_member_id(client):
    
    stdin, stdout, stderr = client.exec_command('sudo zerotier-cli info')

    output = stdout.read().decode('utf8').split("\n")[0].split(" ")

    if len(output[2]) == 10 and output[1] == "info":
        member_id = output[2]
    else:
        member_id = None
    
    stdin.close()
    stdout.close()
    stderr.close()

    return member_id

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


def parse_network_id():
    with open("information/info.txt","r") as info:
        info = info.read().split("\n")
        network_id = info[0].split("=")[-1]
    return network_id

def put_file(local_file, remote_file, client):
    with open(local_file,"r") as file:
            file = file.readlines()

    for index,line in enumerate(file):
        line = line.replace("\n","")
        if index == 0:   
            execute_single_command(f"echo \"{line}\" | sudo tee {remote_file}", client)
        else:
            execute_single_command(f"echo \"{line}\" | sudo tee -a {remote_file}", client)
