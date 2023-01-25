import subprocess
import pandas as pd
import re

jobs = ["crab_2023-01-12/crab_UL2016preVFP_Run2016B"] # list of jobs
schedulerStatuses = [] # list to store scheduler status of each job
jobStatuses = [] # list to store job status of each job

# loop through the list of jobs
for job in jobs:
    # run the status command for each job
    cmdCrabStatus = "crab status -d" + job
    process = subprocess.Popen(cmdCrabStatus, stdout=subprocess.PIPE, shell=True)
    (output, err) = process.communicate()    # parse the output to get the status
    output = output.decode()


    # To get the Scheduler status
    lines = output.split('\n')
    for line in lines:
        if line.startswith("Status on the scheduler:"):
            schedulerStatus = line.split()[-1]
            schedulerStatus = schedulerStatus.encode('utf-8')
            # print()
    schedulerStatuses.append(schedulerStatus)


    ## To get the Job statuses as text string
    startWord = "Jobs status:"
    endWord = "No publication information"
    start_index = output.find(startWord) + len(startWord)
    end_index = output.find(endWord)
    text_between = output[start_index:end_index].strip().encode('utf-8')
    print(text_between)


    # remove leading whitespaces,tabs and newlines
    text_between = re.sub(r'(?m)^[ \t\r\f\v]*', '', text_between)

    # Converting the string into dictionary
    status_regex = re.compile(r'(\w+)\s+([\d.]+)%\s+(\(?)\s*(\d+)/(\d+)\)')
    jobStatus = {}
    for match in status_regex.finditer(text_between):
        #print(match.groups())
        flag, percentage, brace,current, total = match.groups()
	print(flag,percentage,brace,current,total)
        jobStatus[flag] = "%s%% (%s/%s)" % (percentage.encode('utf-8'), current.encode('utf-8'), total.encode('utf-8'))
	print(jobStatus)
    jobStatus = {k.encode('ascii', 'ignore'): v.encode('ascii', 'ignore') for k, v in jobStatus.items()}
    jobStatuses.append(jobStatus)
    print(jobStatuses)

df = pd.DataFrame({'Job': jobs, 'Scheduler Status': schedulerStatuses, 'Job Status': jobStatuses})



# print the table of job status
print(df)
