#Import libraries

from zerotier_src.helper_central import create_network,modify_route,assign_member_ip
from zerotier_src.helper_central import assign_network_name,assign_member_name_desc
from zerotier_src.helper_service import get_node_id,join_network
#from zerotier_env import central_token,service_token

#Two types of token are needed:
#ZeroTier central token:
# Get from Zerotier Central website. Used for central API (creating network)
#ZeroTier service token:
# Get from C:/ProgramData/ZeroTier/One. Used for service API (local zerotier service)

#print(f"Central token: {central_token}")
#print(f"Service token: {service_token}")

def create_join_assign(central_token, service_token):
    try:
        print("Attempting to create network, join network, and assign IP address")

        #Create network
        print("Creating network...")
        create_response = create_network(central_token)
        network_id = create_response["id"]

        #Assigning network name
        network_name = "My_Chyntia"
        print(f"Assigning network name to {network_name}...")
        net_name_response = assign_network_name(central_token, network_id, network_name)

        #Modify route on network
        print("Modifying network route...")
        route_response = modify_route(central_token, network_id, [
            {
                "target":"192.168.231.0/24",
                "via":"null"
            }
        ])

        #Get node address
        print("Getting node address...")
        node_response = get_node_id(service_token)
        node_id = node_response

        #Join network
        print("Joining network...")
        join_response = join_network(service_token, network_id)

        #Assigning member name
        member_name = "GCS"
        member_desc = "My_GCS on Windows"
        print(f"Assigning member name to {member_name} and description to {member_desc}")
        assign_member_name_desc(central_token, network_id, node_id, member_name, member_desc)

        #Assigning new IP
        print("Assigning IP address...")
        assign_response = assign_member_ip(central_token, network_id, node_id, "192.168.231.2")

        print("Process completed.")

        print("Saving information to /information/info.txt.")
        with open("./information/info.txt","w") as info_file:
            lines = [
                f"network_id={network_id}\n",
                f"network_name={network_name}\n",
                f"gcs_node_id={node_id}\n",
                f"gcs_node_name={member_name}"
            ]
            info_file.writelines(lines)
        
        return 0

    except Exception as e:
        print(e)
        return 1

#create_join_assign(central_token, service_token)