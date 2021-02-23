import requests
import base64

from Job import *
from DCAN_API import *

class Provider:
    def __init__(self,server_address,port):
        self.server_address = server_address + ':' + str(port)

    def post_job(self,username,job_title,job_description,shader,dataset):
        self.check_username(username)
        #post job
        url = url_template.format(protocol=PROTOCOL,server_address=self.server_address,uri=JOBS_URI)
        response = requests.post(url,json={'username':username,'title':job_title,'description':job_description})
        created_job = response.json()
        print(created_job)
        print(created_job['id'])
        #post shader
        url = url_template.format(protocol=PROTOCOL,server_address=self.server_address,uri=JOB_ID_SHADER_URI.format(job_id=created_job['id']))
        response = requests.post(url,json={'shader':base64.b64encode(shader).decode('utf-8')})#"{shader_json}".format(shader_json=shader_json))
        #post dataset
        self.post_dataset(created_job['id'],dataset)
        return created_job

    def check_username(self,username):
        url = url_template.format(protocol=PROTOCOL,server_address=self.server_address,uri=USERS_URI)
        response = requests.get(url)
        users = response.json()
        print(users)
        username_valid = False
        for user in users:
            if user['username'] == username:
                username_valid = True
        
        if not username_valid:
            url = url_template.format(protocol=PROTOCOL,server_address=self.server_address,uri=USERS_URI)
            response = requests.post(url,json={'username':username,'password':"null"})
        


    def post_dataset(self,job_id,dataset):
        url = url_template.format(protocol=PROTOCOL,server_address=self.server_address,uri=JOB_ID_DATASET_INFO_URI.format(job_id=job_id))
        response = requests.post(url,json={'data':str(dataset)})
        created_dataset = response.json()
        return created_dataset

    def get_dataset_info(self,job_id):
        url = url_template.format(protocol=PROTOCOL, server_address=self.server_address, uri=JOB_ID_DATASET_INFO_URI.format(job_id = job_id))
        response = requests.get(url)
        return response.json()

    def get_results_by_title(self,job_title):
        url = url_template.format(protocol=PROTOCOL,server_address=self.server_address,uri=JOBS_URI)
        response = requests.get(url)
        job_results = []
        for job in response.json():
            if job_title in job['title']:
                job_results.append(self.get_results(job['id']))
        return job_results

    def get_results(self,job_id):
        results= []
        dataset_info = self.get_dataset_info(job_id)
        for dataset in dataset_info:
            results.append(self.get_result(job_id,dataset['id']))
        return results

    def get_result(self,job_id,dataset_id):
        url = url_template.format(protocol=PROTOCOL,server_address=self.server_address,uri=JOB_ID_DATASET_ID_RESULTS_URI.format(job_id=job_id,dataset_id=dataset_id))
        response = requests.get(url)
        return response.json()


