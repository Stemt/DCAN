import requests
import kp
import base64
import json

from Job import *
from DCAN_API import *


class Worker:
    def __init__(self,server_address,port):
        self.server_address = server_address + ':' + str(port)

    def run_job_by_keyword(self,keywords):
        jobs = self.get_jobs_by_keyword(keywords)
        print("would you like to run the following job:\n{job_title}\n--------------------------------------\n{job_description}\n\nIs this the job you would like to run? [Y/n]:".format(job_title=jobs[0]['title'],job_description=jobs[0]['description']))
        user_response = ""
        valid_inputs = ['y','Y','n','N']
        while len(user_response) < 1 or user_response[0] not in valid_inputs:
            user_response = input()
            if user_response == "" or user_response[0] == 'y' or user_response[0] == 'Y':
                user_response = 'y'
                print("running job..")
                self.run_job(jobs[0]['id'])
                print("done")
            elif user_response[0] == 'n' or user_response[0] == 'N':
                print("exiting..")
                return
            else:
                print("invalid input: \"" + user_response + "\"")

    def run_job(self,job_id):
        #get shader
        shader_dict = self.get_shader(job_id)
        print(shader_dict)
        shader = base64.b64decode(shader_dict['shader'].encode('utf-8'))
        #get dataset
        dataset_info = self.get_dataset_info(job_id)
        dataset = None
        dataset_id = -1
        print("dataset info: " + str(dataset_info))

        for item in dataset_info:
            if item['status'] == "not allocated":
                dataset = self.get_dataset(job_id,item['id'])
                dataset_id = item['id']
                break

        #run shader with dataset
        shader_op_argument_lists = []

        mgr = kp.Manager()

        print("raw string:")
        print(dataset['data'])
        dataset = json.loads(dataset['data'])
        dataset = "".join(dataset)
        dataset = json.loads(dataset)
        print(dataset['data'])

        #import data and load into shaders
        for row in dataset['data']:
            shader_op_tensors = []
            for value in row:
                if value != type([]):
                    value = [value]
                print("loading value: ")
                print(value)
                shader_op_tensors.append(mgr.build_tensor(value))
            shader_op_argument_lists.append(shader_op_tensors)
        

        #copy data to gpu and executa asynchronously
        for arg_list in shader_op_argument_lists:
            mgr.eval_tensor_sync_device_def(arg_list)
            mgr.eval_async_algo_data_def(arg_list,shader)

        results= []

        for arg_list in shader_op_argument_lists:
            #wait until shader is done executing
            mgr.eval_await_def()
            #copy data back to local memory
            mgr.eval_tensor_sync_local_def(arg_list)

            result_list = []

            #put results into a list
            for arg in arg_list:
                result_list.append(arg.data())

            results.append(result_list)
        
        self.post_results(job_id,dataset_id,results)
        
    def post_results(self,job_id,dataset_id,results):
        url = url_template.format(protocol=PROTOCOL, server_address=self.server_address, uri=JOB_ID_DATASET_ID_RESULTS_URI.format(job_id = job_id, dataset_id = dataset_id))
        response = requests.post(url,json={'results':results})
        if response.status_code != 200:
            print("failed to post results. code: "+response.status)

    def get_jobs_by_keyword(self,keywords):
        jobs = self.get_jobs()
        sought_jobs = []
        for job in jobs:
            for keyword in keywords:
                if keyword in job['title'] or keyword in job['description']:
                    sought_jobs.append(job)
        return sought_jobs

    def get_jobs(self):
        url = url_template.format(protocol=PROTOCOL, server_address=self.server_address, uri=JOBS_URI)
        response = requests.get(url)
        return response.json()

    def get_job(self,job_id):
        url = url_template.format(protocol=PROTOCOL, server_address=self.server_address, uri=JOB_ID_URI.format(job_id = job_id))
        response = requests.get(url)
        return response.json()

    def get_shader(self,job_id):
        url = url_template.format(protocol=PROTOCOL, server_address=self.server_address, uri=JOB_ID_SHADER_URI.format(job_id = job_id))
        response = requests.get(url)
        return response.json()

    def get_dataset_info(self,job_id):
        url = url_template.format(protocol=PROTOCOL, server_address=self.server_address, uri=JOB_ID_DATASET_INFO_URI.format(job_id = job_id))
        response = requests.get(url)
        return response.json()

    def get_dataset(self,job_id,dataset_id):
        url = url_template.format(protocol=PROTOCOL, server_address=self.server_address, uri=JOB_ID_DATASET_ID_URI.format(job_id = job_id, dataset_id = dataset_id))
        response = requests.get(url)
        return response.json()




