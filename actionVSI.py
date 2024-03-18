import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

#Authenticate user on IBM Cloud to do VPC VSI commands
authenticator = IAMAuthenticator(os.environ.get('key'), url='https://iam.cloud.ibm.com')


#  Listing VPCs
print("List VPCs")
try:
    vpcs = service.list_vpcs().get_result()['vpcs']
except ApiException as e:
  print("List VPC failed with status code " + str(e.code) + ": " + e.message)
for vpc in vpcs:
    print(vpc['id'], "\t",  vpc['name'])

#  Listing Subnets
print("List Subnets")
try:
    subnets = service.list_subnets().get_result()['subnets']
except ApiException as e:
  print("List subnets failed with status code " + str(e.code) + ": " + e.message)
for subnet in subnets:
    print(subnet['id'], "\t",  subnet['name'])

#  Listing Instances
print("List Instances")
try:
    instances = service.list_instances().get_result()['instances']
except ApiException as e:
  print("List instances failed with status code " + str(e.code) + ": " + e.message)
for instance in instances:
    print(instance['id'], "\t",  instance['name'])


#  Updating Instance
print("Updated Instance")
try:
    newInstanceName = instanceName + "-1"
    instance = service.update_instance(
        id=instanceId,
        name=newInstanceName,
    ).get_result()
except ApiException as e:
    print("Update instance failed with status code " + str(e.code) + ": " + e.message)
print(instance['id'], "\t",  instance['name'])
