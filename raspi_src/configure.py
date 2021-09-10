import time
#from raspi_env import central_token
from paramiko import SSHClient, AutoAddPolicy
from raspi_src.helper_raspi import execute_single_command,get_zerotier_member_id
from raspi_src.helper_raspi import assign_member_ip,assign_member_name_desc,parse_network_id,put_file

def configure_raspi(central_token, raspi_host="raspberrypi",raspi_user="pi",raspi_password="raspberry",update=True):
    try:
        with SSHClient() as client:

            print("Connecting to Raspberry Pi...")
            client.set_missing_host_key_policy(AutoAddPolicy())
            for i in range(5):
                try:
                    client.connect(raspi_host, username=raspi_user, password=raspi_password)
                    print("Connected.")
                    break
                except:
                    if i != 4:
                        print("Couldn't connect to Raspberry Pi. Waiting for 5 secs and retrying...")
                        time.sleep(5)
                    else:
                        print("Couldn't connect to Raspberry Pi.")

            if update:
                print("Updating packages...")
                execute_single_command('sudo apt-get update --allow-releaseinfo-change && sudo apt-get upgrade -y', client)
            
            print("Installing zerotier...")
            execute_single_command('curl -s https://install.zerotier.com | sudo bash', client)

            raspi_zerotier_id = get_zerotier_member_id(client)
            network_id = parse_network_id()

            print("Joining zerotier network...")
            execute_single_command(f"sudo zerotier-cli join {network_id}", client)

            print("Assigning IP address, name, and description to Raspberry Pi...")
            assign_member_ip(central_token, network_id, raspi_zerotier_id, "192.168.231.3")
            assign_member_name_desc(central_token, network_id, raspi_zerotier_id, "RasPi", "Raspberry Pi!")

            print("Done configuring zerotier.")

            print("Installing Mavlink Router...")

            print("Cloning Mavlink Router repository...")
            execute_single_command("sudo apt install git -y", client)

            print("Building Mavlink Router...")
            execute_single_command("git clone https://github.com/mavlink-router/mavlink-router.git", client)
            execute_single_command("cd mavlink-router && git submodule update --init --recursive", client)
            execute_single_command("sudo apt install python-future -y", client)
            execute_single_command("sudo apt install python3-future -y", client)
            execute_single_command("sudo apt install libtool -y", client)
            execute_single_command("sudo apt install autoconf -y", client)

            execute_single_command("cd mavlink-router && sudo ./autogen.sh && sudo ./configure CFLAGS='-g -O2' --sysconfdir=/etc --localstatedir=/var --libdir=/usr/lib --prefix=/usr", client)
            execute_single_command("cd mavlink-router && sudo make",client)
            execute_single_command("cd mavlink-router && sudo make install",client)
            execute_single_command("sudo mkdir /etc/mavlink-router",client)
            execute_single_command("sudo touch /etc/mavlink-router/main.conf",client)

            put_file("raspi_src/config_template/main.conf","/etc/mavlink-router/main.conf",client)
            put_file("raspi_src/config_template/mavlink-router.service","/lib/systemd/system/mavlink-router.service",client)

            print("Enabling Mavlink Router service")
            execute_single_command("sudo systemctl enable mavlink-router",client)
            execute_single_command("sudo systemctl start mavlink-router",client)

            print("Done configuring Mavlink Router.")

            print("Done configuring Raspberry Pi.")
            print("When module is ON, packets will be sent to port 14550.")
        
        return 0

    except Exception as e:
        print(e)
        return 1
