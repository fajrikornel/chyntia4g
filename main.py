import sys
from getpass import getpass
from zerotier_src.zerotier import create_join_assign
from raspi_src.initialize import initialize_raspi
from raspi_src.configure import configure_raspi

advanced = input("Simple setup or advanced mode? Input \"a\" or \"A\" for advanced mode. Anything else means simple mode: ")

if advanced:
    print("Stages:")
    print("1. User input")
    print("2. Initialize GCS (Create, join, configure ZeroTier network")
    print("3. Initialize Raspberry Pi")
    print("4. Configure Rasberry Pi")
    stages = input("Input the stages you want to execute (example: 14): ")
    stages = list(stages)
    stages = [int(x) for x in stages]
else:
    stages = [1,2,3,4]

if 1 in stages:
    print("Stage 1: User input.")

    central_token = getpass("Input your ZeroTier Central token: ")
    service_token = getpass("Input your ZeroTier Service token: ")
    if 3 in stages:
        country = input("Input your two-letter country code: ")
        wifi_ssid = input("Input the 4G Wi-Fi SSID: ")
        wifi_password = getpass("Input the 4G Wi-Fi password: ")
        print("Please insert the Raspberry Pi SD Card onto the computer.")
        raspi_boot_dir = input("Input the absolute directory of the Raspberry Pi /boot SD card: ")
    if 4 in stages:
        raspi_host = input("Input the Raspberry Pi host (Enter if default): ")
        raspi_user = input("Input the Raspberry Pi user (Enter if default): ")
        raspi_password = getpass("Input the Raspberry Pi user password (Enter if default): ")

        update = None
        while (update != True and update != False):
            update = input("Would you like to update the Raspberry Pi packages? (y/n): ")
            if update.lower() != 'y' and update.lower() != 'n':
                print("Please input y or n.")
            elif update.lower() == 'y':
                update = True
            elif update.lower() == 'n':
                update = False

        if raspi_host == '':
            raspi_host = 'raspberrypi'
        if raspi_user == '':
            raspi_user = 'pi'
        if raspi_password == '':
            raspi_password = 'raspberry'

if 2 in stages:
    print("Stage 2: Setting up Ground Control Station.")

    exit_code_2 = create_join_assign(central_token,service_token)
    if exit_code_2 != 0:
        print("Error while executing stage 2. Program will exit.")
        sys.exit(1)
    else:
        print("Stage 2 done.")


if 3 in stages:
    print("Stage 3: Initializing Raspberry Pi.")
    print("Please make sure the Raspberry Pi SD Card is attached to the computer.")

    exit_code_3 = initialize_raspi(raspi_boot_dir, country, wifi_ssid, wifi_password)
    if exit_code_3 != 0:
        print("Error while executing stage 3. Program will exit.")
        sys.exit(1)
    else:
        print("Stage 3 done.")

if 4 in stages:
    print("Stage 4: Configuring Raspberry Pi.")

    print("Please remove the SD card from the computer and attach it to the Raspberry Pi.")
    print("Turn the Raspberry Pi on and wait for it to boot. This may take a few minutes.")
    print("Make sure the 4G Wi-Fi module is on and has internet service.")
    print("Connect this computer to the 4G Wi-Fi module.")
    print("If user wants to ensure Raspberry Pi is fully booted, open up a new terminal and try to ping the Raspberry Pi.")

    raspi_boot_done = False
    while not raspi_boot_done:
        print("Waiting for the Raspberry Pi to fully boot.")
        raspi_boot_done = input("Is the Raspberry Pi fully booted yet? (y/n/cancel): ")
        raspi_boot_done = raspi_boot_done.lower()
        if raspi_boot_done == 'y':
            raspi_boot_done = True
        elif raspi_boot_done == 'n':
            raspi_boot_done = False
        elif raspi_boot_done == 'cancel':
            print("User has decided to cancel execution. Program will now exit.")
            sys.exit(2)

    exit_code_4 = configure_raspi(central_token, raspi_host, raspi_user, raspi_password, update)
    if exit_code_4 != 0:
        print("Error while executing stage 4. Program will exit.")
        sys.exit(1)
    else:
        print("Stage 4 done.")

print("Program ran successfully.")
sys.exit(0)

#EXIT CODES GUIDE:
#0: Successful execution
#1: Unsuccessful execution
#2: User stopped execution