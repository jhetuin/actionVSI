import os
from ibm_vpc import VpcV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

#Authenticate user on IBM Cloud to do VPC VSI commands
authenticator = IAMAuthenticator(os.environ.get('key'), url='https://iam.cloud.ibm.com')
service = VpcV1(authenticator=authenticator)

#or
#API_KEY = os.environ['api_key']
#authenticator = IAMAuthenticator(API_KEY)

#Set API endpoints
#service.set_service_url('https://eu-gb.iaas.cloud.ibm.com/v1')
service.set_service_url('https://' +region+ 'eu-gb.iaas.cloud.ibm.com/v1')
#service.set_service_url('https://api.eu-gb.codeengine.cloud.ibm.com/v2')


#Get the required action from environment variable
VSIaction = os.environ['action']

# List of instance ID to perform action
instance_ids = []

# Read list from environment variables (assume there will not be more that 5 VSIs)
for VSI in range(1,5):
    try:
        instance_ids.append(os.environ['VSI_' + str(VSI)])
    except:
        break

# Perform action on list
for instance_id in instance_ids:
    print(instance_id)
    response = service.create_instance_action(
        instance_id,
        type = VSIaction,
    )
