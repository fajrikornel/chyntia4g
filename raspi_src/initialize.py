#Three steps of setup:
#1. Enable uart in config.txt (enable_uart=1)
#2. Enable ssh (add ssh file)
#3. Add wifi_supplicant.conf

#from raspi_env import raspi_boot_dir,country,wifi_ssid,wifi_password
from raspi_src.helper_raspi import enable_uart_config,enable_wifi_config
import re

def initialize_raspi(raspi_boot_dir,country,wifi_ssid,wifi_password):
    try:
        raspi_boot_dir = raspi_boot_dir[:-1] + raspi_boot_dir[-1].replace("/","") #Ensuring no "/" for last character

        ###############
        #Enabling uart#
        ###############

        print("Enabling UART...\n")

        with open(f"{raspi_boot_dir}/config.txt","r") as config_file:
            print("Reading config.txt file\n")
            config_file_list = config_file.readlines()

        config_file_list = enable_uart_config(config_file_list)

        #print(config_file_list)

        with open(f"{raspi_boot_dir}/config.txt","w") as config_file:
            print("Writing config.txt file\n")
            config_file.writelines(config_file_list)

        ##############
        #Enabling SSH#
        ##############

        print("Enabling SSH...\n")

        with open(f"{raspi_boot_dir}/ssh", "w") as ssh_file:
            pass

        ################
        #Enabling Wi-Fi#
        ################

        print("Enabling Wi-Fi...\n")

        with open(f"{raspi_boot_dir}/wpa_supplicant.conf", "w") as wifi_file:
            wifi_config_list = enable_wifi_config(country, wifi_ssid, wifi_password)
            wifi_file.writelines(wifi_config_list)
        
        return 0

    except Exception as e:
        print(e)
        return 1