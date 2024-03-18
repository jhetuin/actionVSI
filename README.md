Step-by-step instructions

Now to get this scheduled and running in Code Engine, you’ll need to go through the steps below:

Install the IBM Cloud CLI with Code Engine module by following the instructions on IBM Cloud Docs.

Create the project:

Command:

ibmcloud ce project create -n Test_Instance_StartAndStop

Select the project:

Command:

ibmcloud ce project select -n Test_Instance_StartAndStop

Create API secrets:

Command (remember to substitute your API KEY for the value <YourApiKey>):

ibmcloud ce secret create --name api-key --from-literal "api_key=<Your API Key>"

Create the VSI configmap:

Command:

ibmcloud ce configmap create --name vsi-id --from-env-file ../vsi-id.txt

Contents of the file:

Command:

cat ../vsi-id.txt

Sample output:

VSI_1=02u7_a9941f61-e7eb-4ce6-8935-c02471d3d0bd
VSI_2=02u7_0a7effa8-e8e0-44da-ab50-68786f830b42
VSI_3=02u7_d7a22fdd-f5af-4179-b489-3450669b306d
VSI_4=02u7_d3077e84-9d93-48f2-80ca-2e21a053d548
VSI_5=02u7_7dbb4c31-ab13-4469-894a-f040d4b8d418

Create actions start and stop literal variables:

Command:

ibmcloud ce configmap create --name action-start --from-literal action=start

Sample output:

Creating configmap 'action-start'...
OK
Run 'ibmcloud ce configmap get -n action-start' to see more details.

Command:

ibmcloud ce configmap create --name action-stop --from-literal action=stop

Sample output:

Creating configmap 'action-stop'...
OK
Run 'ibmcloud ce configmap get -n action-stop' to see more details.

Create the job for starting the instances by using all that we’ve created so far (VSI configmap data set, secret API key and the action). You’ll also set the CPU and Memory requirements for the lowest possible setting (1/8 CPU and 250 MB of memory):

Command:

ibmcloud ce job create --name actionvsi-start --build-source . --wait --cpu .125 --memory .25G --env-from-secret api-key --env-from-configmap vsi-id --env-from-configmap action-start

Sample output:

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

Create a job for stopping the instances, just as we did for starting:

Command:

ibmcloud ce job create --name actionvsi-stop --build-source . --wait --cpu .125 --memory .25G --env-from-secret api-key --env-from-configmap vsi-id --env-from-configmap action-stop

Sample output:

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

If you are curious, you can check on the UI — Code Engine > Projects > Your Project Name > Jobs and click on the star job, then Configuration, then Environment variables:
If you are curious, you can check on the UI — Code Engine > Projects > Your Project Name > Jobs and click on the star job, then Configuration, then Environment variables:

You can also follow the job runs, submit jobs and do everything else through the UI, should you choose to do so. I prefer to stick to CLI as I find it easier to document.

Time to test the jobs we have created. As you can see below, there are five instances that end in vsi-0-01 — these are my test instances for this script. They are all in a stopped state:
Time to test the jobs we have created. As you can see below, there are five instances that end in vsi-0-01 — these are my test instances for this script. They are all in a stopped state:

Let’s run the start job and turn the instances on (or to a started state):

Command:

ibmcloud ce jobrun submit --name start-test-run --job actionvsi-start

Sample output:

Getting job 'actionvsi-start'...
Submitting job run 'start-test-run'...
Run 'ibmcloud ce jobrun get -n start-test-run' to check the job run status.
OK

Optionally, you can check on the state of the job run by executing the suggested command, so let’s do that:

Command:

ibmcloud ce jobrun get -n start-test-run

Sample output:

Getting jobrun 'start-test-run'...
Getting instances of jobrun 'start-test-run'...
Getting events of jobrun 'start-test-run'...
Run 'ibmcloud ce jobrun events -n start-test-run' to get the system events of the job run instances.
Run 'ibmcloud ce jobrun logs -f -n start-test-run' to follow the logs of the job run instances.
OK

Name:          start-test-run  
ID:            d051f6a5-6026-429d-92ce-c7626b4115ed  
Project Name:  Test_Instance_StartAndStop
Project ID:    bfe86bd8-e9e4-4aef-8b21-f53635404fda  
Age:           52s  
Created:       2022-05-06T12:36:35-04:00  

Job Ref:                actionvsi-start  
Environment Variables:    
  Type                      Name          Value  
  ConfigMap full reference  action-start    
  ConfigMap full reference  vsi-id          
  Secret full reference     api-key         
Image:                  private.us.icr.io/ce--3fe45-nlg73169h4n/job-actionvsi-start  
Resource Allocation:      
  CPU:                0.125  
  Ephemeral Storage:  400M  
  Memory:             250M  
Registry Secrets:         
  ce-auto-icr-private-us-south  

Runtime:      
  Array Indices:       0  
  Max Execution Time:  7200  
  Retry Limit:         3  

Status:       
  Completed:          11s  
  Instance Statuses:    
    Succeeded:  1  
  Conditions:         
    Type      Status  Last Probe  Last Transition  
    Pending   True    51s         51s  
    Running   True    31s         31s  
    Complete  True    11s         11s  

Events:       
  Type    Reason     Age                Source                Messages  
  Normal  Updated    12s (x4 over 52s)  batch-job-controller  Updated JobRun "start-test-run"  
  Normal  Completed  12s                batch-job-controller  JobRun completed successfully  

Instances:    
  Name                Running  Status     Restarts  Age  
  start-test-run-0-0  0/1      Succeeded  0         52s

Optionally, you can also check the state via the UI:
Optionally, you can also check the state via the UI:

Once the job has finished successfully, we can go back and check on the instances:
Once that the job has finished successfully, we can go back and check on the instances:

Test successful! Now repeat for the stop action.

Test stopping all the instances:

Command:

ibmcloud ce jobrun submit --name stop-test-run --job actionvsi-stop

Sample output:

Getting job 'actionvsi-stop'...
Submitting job run 'stop-test-run'...
Run 'ibmcloud ce jobrun get -n stop-test-run' to check the job run status.
OK

Check if the job ran successfully:

Command:

ibmcloud ce jobrun get -n stop-test-run

Sample output:

Getting jobrun 'stop-test-run'...
Getting instances of jobrun 'stop-test-run'...
Getting events of jobrun 'stop-test-run'...
Run 'ibmcloud ce jobrun events -n stop-test-run' to get the system events of the job run instances.
Run 'ibmcloud ce jobrun logs -f -n stop-test-run' to follow the logs of the job run instances.
OK

Name:          stop-test-run  
ID:            18c1952b-0892-4f2d-be2c-47fb3e4cf4e0  
Project Name:  Test_Instance_StartAndStop  
Project ID:    bfe86bd8-e9e4-4aef-8b21-f53635404fda  
Age:           21s  
Created:       2022-05-06T12:39:18-04:00  

Job Ref:                actionvsi-stop  
Environment Variables:    
  Type                      Name         Value  
  ConfigMap full reference  action-stop    
  ConfigMap full reference  vsi-id         
  Secret full reference     api-key        
Image:                  private.us.icr.io/ce--3fe45-nlg73169h4n/job-actionvsi-stop  
Resource Allocation:      
  CPU:                0.125  
  Ephemeral Storage:  400M  
  Memory:             250M  
Registry Secrets:         
  ce-auto-icr-private-us-south  

Runtime:      
  Array Indices:       0  
  Max Execution Time:  7200  
  Retry Limit:         3  

Status:       
  Completed:          3s  
  Instance Statuses:    
    Succeeded:  1  
  Conditions:         
    Type      Status  Last Probe  Last Transition  
    Pending   True    21s         21s  
    Running   True    12s         12s  
    Complete  True    3s          3s  

Events:       
  Type    Reason     Age               Source                Messages  
  Normal  Updated    3s (x4 over 21s)  batch-job-controller  Updated JobRun "stop-test-run"  
  Normal  Completed  3s                batch-job-controller  JobRun completed successfully  

Instances:    
  Name               Running  Status     Restarts  Age  
  stop-test-run-0-0  0/1      Succeeded  0         21s

Again, you can also check via the UI:
Again, you can also check via the UI:

Let’s check the instances once more to see that all the five resources with VSI at the end (the same set that were started) are now stopped:
Let’s check the instances once more to see that all the five resources with VSI at the end (the same set that were started) are now stopped:

Now that we’re certain both jobs work, we can schedule them with CRON:

Turns on at 7:00 AM (Sao Paulo, Brazil time zone) every weekday:

Command:

ibmcloud ce sub cron create --name cron-sub-actionvsi-start --destination actionvsi-start --destination-type job --schedule '0 7 * * 1-5' --time-zone "America/Sao_Paulo"

Sample output:

Creating cron event subscription 'cron-sub-actionvsi-start'...
Run 'ibmcloud ce subscription cron get -n cron-sub-actionvsi-start' to check the cron event subscription status.
OK

Turns off at 7:00 PM every weekday:

Command:

ibmcloud ce sub cron create --name cron-sub-actionvsi-stop --destination actionvsi-stop --destination-type job --schedule '0 19 * * 1-5' --time-zone "America/Sao_Paulo"

Sample output:

Creating cron event subscription 'cron-sub-actionvsi-stop'...
Run 'ibmcloud ce subscription cron get -n cron-sub-actionvsi-stop' to check the cron event subscription status.
OK

Learn more

The blog post describes how you can use IBM Cloud Code Engine to run a scheduled script that will perform any desired actions via API on IBM Cloud. In this example, we explored turning a set of VSIs (Virtual Server Instances) on and off at a specific time of the day, which is useful because it reduces costs by turning off infrastructure when it is not needed.
