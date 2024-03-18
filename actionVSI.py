import os
from ibm_vpc import VpcV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#Authenticate user on IBM Cloud to do VPC VSI commands
API_KEY = os.environ['api_key']
authenticator = IAMAuthenticator(os.environ.get('api_key'), url='https://iam.cloud.ibm.com')
#authenticator = IAMAuthenticator(API_KEY)
service = VpcV1(authenticator=authenticator)


#Set API endpoints
service.set_service_url('https://br-sao.iaas.cloud.ibm.com/v1')

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
