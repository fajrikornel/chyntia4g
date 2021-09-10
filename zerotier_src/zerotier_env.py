############
#DEPRECATED#
############

import os
from dotenv import load_dotenv

load_dotenv('../.env')

central_token = os.getenv('central_token')
service_token = os.getenv('service_token')
