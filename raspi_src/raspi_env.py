############
#DEPRECATED#
############

import os
from dotenv import load_dotenv

load_dotenv('../.env')

raspi_boot_dir = os.getenv('raspi_boot_dir')
country = os.getenv("country") #POSSIBILITY OF COUNTRY=CHINA BECAUSE OF 4G LTE MODULE
wifi_ssid = os.getenv("wifi_ssid")
wifi_password = os.getenv("wifi_password")
central_token = os.getenv("central_token")