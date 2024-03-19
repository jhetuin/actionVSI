
# Project Title

A brief description of what this project does and who it's for


## Deployment

To deploy this project run [Install the IBM Cloud CLI with Code Engine module](https://cloud.ibm.com/docs/codeengine?topic=codeengine-install-cli) by following the instructions on IBM Cloud Docs.

Create the project:

```bash
ibmcloud ce project create -n Test_Instance_StartAndStop
```

Select the project:
```bash
ibmcloud ce project select -n Test_Instance_StartAndStop
```

Create API secrets (remember to substitute your API KEY for the value <YourApiKey>):
```bash
ibmcloud ce secret create --name api-key --from-literal key="<Your API Key>"
```

Create region literal variables (remember to substitute your region (example eu-gb) for the value <Your-Region>):
```bash
ibmcloud ce configmap create --name location --from-literal region=<Your-Region>
```
Sample output:
```bash
Creating configmap 'location'...
OK
Run 'ibmcloud ce configmap get -n location' to see more details.
```

Create the VSI configmap:
```bash
ibmcloud ce configmap create --name vsi-id --from-env-file ../vsi-id.txt
```

Contents of the file:

Sample output:
```bash
VSI_1=02u7_a9941f61-e7eb-4ce6-8935-c02471d3d0bd
VSI_2=02u7_0a7effa8-e8e0-44da-ab50-68786f830b42
VSI_3=02u7_d7a22fdd-f5af-4179-b489-3450669b306d
VSI_4=02u7_d3077e84-9d93-48f2-80ca-2e21a053d548
VSI_5=02u7_7dbb4c31-ab13-4469-894a-f040d4b8d418
```

Create actions start and stop literal variables:
```bash
ibmcloud ce configmap create --name action-start --from-literal action=start
```
Sample output:
```bash
Creating configmap 'action-start'...
OK
Run 'ibmcloud ce configmap get -n action-start' to see more details.
```

```bash
ibmcloud ce configmap create --name action-stop --from-literal action=stop
```

Sample output:
```bash
Creating configmap 'action-stop'...
OK
Run 'ibmcloud ce configmap get -n action-stop' to see more details.
```


Create the job for starting the instances by using all that we’ve created so far (VSI configmap data set, secret API key and the action). You’ll also set the CPU and Memory requirements for the lowest possible setting (1/8 CPU and 250 MB of memory):

Command:
```bash
ibmcloud ce job create --name actionvsi-start --build-source https://github.com/jhetuin/actionVSI.git --wait --cpu .125 --memory .25G --env-from-secret key --env-from-configmap location --env-from-configmap vsi-id --env-from-configmap action-start
```

Sample output:
```bash
Creating job 'actionvsi-start'...
Creating build 'actionvsi-start-build-220506-122817967'...
Packaging files to upload from source path '.'...
Submitting build run 'actionvsi-start-run-220506-122817967'...
Creating image 'private.us.icr.io/ce--3fe45-nlg73169h4n/job-actionvsi-start'...
Waiting for build run to complete...
Build run status: 'Running'
Build run completed successfully.
Run 'ibmcloud ce buildrun get -n actionvsi-start-run-220506-122817967' to check the build run status.
OK
```
Create a job for stopping the instances, just as we did for starting:

Command:
```bash
ibmcloud ce job create --name actionvsi-stop --build-source https://github.com/jhetuin/actionVSI.git --wait --cpu .125 --memory .25G --env-from-secret api-key --env-from-configmap location --env-from-configmap vsi-id --env-from-configmap action-stop
```

Sample output:
```bash
Creating job 'actionvsi-stop'...
Creating build 'actionvsi-stop-build-220506-123157457'...
Packaging files to upload from source path '.'...
Submitting build run 'actionvsi-stop-run-220506-123157457'...
Creating image 'private.us.icr.io/ce--3fe45-nlg73169h4n/job-actionvsi-stop'...
Waiting for build run to complete...
Build run status: 'Running'
Build run completed successfully.
Run 'ibmcloud ce buildrun get -n actionvsi-stop-run-220506-123157457' to check the build run status.
OK
```


