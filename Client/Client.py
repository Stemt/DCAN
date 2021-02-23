#!/bin/python
import sys
import json

from Worker import *
from JobProvider import *

usage_instruction = """usage: dcan [command] [arg1,arg2,..]
options:
 help: show help
 search KEYWORD [KEYWORD ...]: search for jobs
 process KEYWORD [KEYWORD ...]: work on given job
 post USERNAME SHADER.spirv DATASET.csv [DATASET.csv ...]: post a new job to the network
 results JOBNAME [JOBNAME ...]: get results for given job
 """

if len(sys.argv) < 2:
    print(usage_instruction)
    exit()
elif sys.argv[1] == 'search' and len(sys.argv) > 2:
    worker = Worker('127.0.0.1',5000)
    keywords = []
    for i in range(2,len(sys.argv)):
        keywords.append(sys.argv[i])
    print(worker.get_jobs_by_keyword(keywords))
elif sys.argv[1] == 'process' and len(sys.argv) > 2:
    worker = Worker('127.0.0.1',5000)
    keywords = []
    for i in range(2,len(sys.argv)):
        keywords.append(sys.argv[i])
    worker.run_job_by_keyword(keywords)

elif sys.argv[1] == 'post' and len(sys.argv) > 4:
    provider = Provider('127.0.0.1',5000)
    username = sys.argv[2]
    shader = None
    datasets = ""
    with open(sys.argv[3],'rb') as shader_file:
        shader = shader_file.read()
        print(shader)
    with open(sys.argv[4]) as dataset_file:
        datasets = dataset_file.readlines()
    provider.post_job(username,'new_job','new job',shader,datasets)
    print('job should be posted')
elif sys.argv[1] == 'results':
    provider = Provider('127.0.0.1',5000)
    for i in range(2,len(sys.argv)):
        print(provider.get_results_by_title(sys.argv[i]))
else:
    print(usage_instruction)
    exit()