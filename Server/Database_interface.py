import sqlite3
import json
import base64
from passlib.hash import pbkdf2_sha256

USER_USERNAME_COL = 0
USER_PASSWORD_HASH_COL = 1

JOB_ID_COL = 0
JOB_USERNAME_COL = 1
JOB_TITLE_COL = 2
JOB_DESCRIPTION_COL = 3
JOB_STATUS_COL = 4

SHADER_ID_COL = 0
SHADER_JOB_ID_COL = 1
SHADER_SHADER_COL = 2

DATASET_ID_COL = 0
DATASET_JOB_ID_COL = 1
DATASET_DATA_COL = 2
DATASET_RESULT_COL = 3
DATASET_STATUS_COL = 4

#TODO check all db.execute queries for arguments that should be lists

def get_db():
    conn = sqlite3.connect('DCAN.db')
    return conn

def hash_password(password):
    return pbkdf2_sha256.hash(password, rounds=200000, salt_size=16)

def verify_password(password,hash):
    return pbkdf2_sha256.verify(password,hash)

#user operations
def get_users():
    db = get_db()
    cursor = db.execute("select * from users")
    users = []
    for row in cursor:
        users.append({'username':row[USER_USERNAME_COL]})
    db.close()
    return users

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.execute("select * from users where id = ?",user_id)
    user = None
    for row in cursor:
        user = {'username':row[USER_USERNAME_COL]}
    db.close()
    return user

def get_user_by_name(username):
    db = get_db()
    cursor = db.execute("select * from users where username = ?",[username])
    user = None
    for row in cursor:
        user = {'username':row[USER_USERNAME_COL]}
    db.close()
    return user

def create_user(username,password):
    db = get_db()
    password_hash = hash_password(password)
    db.execute("insert into users (username, password_hash) values (?,?)",[username,password_hash])
    db.commit()
    db.close()
    return True

def verify_user(username,password):
    db =get_db()
    cursor =db.execute("select * from users where username = ?",[username])
    for row in cursor:
        return verify_password(password,row[USER_PASSWORD_HASH_COL])


#job operations
def get_jobs():
    db = get_db()
    cursor = db.execute("select * from jobs")
    jobs = []
    for row in cursor:
        jobs.append({'id':row[JOB_ID_COL],'username':row[JOB_USERNAME_COL],'title':row[JOB_TITLE_COL],'description':row[JOB_DESCRIPTION_COL],'status':row[JOB_STATUS_COL]})
    db.close()
    print(jobs)
    return jobs

def get_job_by_id(job_id):
    db = get_db()
    cursor = db.execute("select * from jobs where id = ?",[job_id])
    job = None
    for row in cursor:
        user = {'id':row[JOB_ID_COL],'username':row[JOB_USERNAME_COL],'title':row[JOB_TITLE_COL],'description':row[JOB_DESCRIPTION_COL],'status':row[JOB_STATUS_COL]}
    db.close()
    return job

def get_shader(job_id):
    db = get_db()
    cursor = db.execute("select * from shaders where job_id = ?",[job_id])
    shader = None
    for row in cursor:
        shader = {'id':row[SHADER_ID_COL], 'job_id':row[SHADER_JOB_ID_COL], 'shader':row[SHADER_SHADER_COL]}
    db.close()
    return shader

def get_datasets(job_id):
    db = get_db()
    cursor = db.execute("select * from datasets where job_id = ?",[job_id])
    datasets = []
    for row in cursor:
        datasets.append({'id':row[DATASET_ID_COL], 'job_id':row[DATASET_JOB_ID_COL], 'status':row[DATASET_STATUS_COL]})
    db.close()
    return datasets

#TODO split into two functions (seperate one for website so it doesn't change the status when dataset is requested)
def get_dataset_by_id(job_id,dataset_id):
    db = get_db()
    cursor = db.execute("select * from datasets where id = ? and job_id = ?",[dataset_id,job_id])
    dataset =  None
    for row in cursor:
        dataset = {'id':row[DATASET_ID_COL], 'job_id':row[DATASET_JOB_ID_COL], 'data':row[DATASET_DATA_COL], 'result':row[DATASET_RESULT_COL], 'status':row[DATASET_STATUS_COL]}
    
    #assumes this is being requested by worker and so updates dataset status
    db.execute("update datasets set status = ? where id = ? and job_id = ?",["not allocated",dataset_id,job_id])#TODO change not allocated to allocated
    db.commit()
    db.close()
    return dataset

def get_dataset_by_id_results(job_id,dataset_id):
    db = get_db()
    cursor = db.execute("select * from datasets where job_id = ? and id = ?",[job_id,dataset_id])
    result = None
    for row in cursor:
        result = {'id':row[DATASET_ID_COL],'job_id':row[DATASET_JOB_ID_COL],'result':row[DATASET_RESULT_COL]}
    db.close()
    return result

#BUG: function may return wrong id of created job if user has already made a job with the same name previously
#(solution) restrict the job title per user
#TODO document
def create_job(username,title,description):
    db = get_db()
    db.execute("insert into jobs (username, job_title, job_description, job_status) values (?,?,?,?)",[username,title,description,"not worked on"])
    db.commit()
    cursor = db.execute("select * from jobs where username = ? and job_title = ?",[username,title])
    created_job = None
    for row in cursor:
        created_job = {'id':row[JOB_ID_COL],'username':row[JOB_USERNAME_COL],'title':row[JOB_TITLE_COL],'description':row[JOB_DESCRIPTION_COL],'status':row[JOB_STATUS_COL]}
    db.close()
    return created_job

#TODO return created entry
def create_shader(job_id,shader):
    db = get_db()
    print(shader)
    db.execute("insert into shaders (job_id, shader) values (?,?)",[job_id,shader])
    db.commit()
    cursor = db.execute("select * from shaders where job_id = ?",[job_id])
    created_shader = None
    for row in cursor:
        created_shader = {'id':row[SHADER_ID_COL],'job_id':row[SHADER_JOB_ID_COL],'data':row[SHADER_SHADER_COL]}
    db.close()
    return created_shader

#TODO return created entry
def create_dataset(job_id,data):
    db = get_db()
    print(data)
    db.execute("insert into datasets (job_id, data, status) values (?,?,?)",[job_id,data,"not allocated"])
    db.commit()
    cursor = db.execute("select * from datasets where job_id = ? and data = ?",[job_id,data])
    created_dataset = None
    for row in cursor:
        created_dataset = {'id':row[DATASET_ID_COL],'job_id':row[DATASET_JOB_ID_COL],'data':row[DATASET_DATA_COL],'result':row[DATASET_RESULT_COL],'status':row[DATASET_STATUS_COL]}
    db.close()
    return created_dataset

#TODO return created entry
def post_result(job_id,dataset_id,results):
    db = get_db()
    print(results)
    db.execute("update datasets set result = ? where job_id = ? and id = ?",[str(results),job_id,dataset_id])
    db.commit()
    cursor = db.execute("select * from datasets where id = ? and job_id = ?",[dataset_id,job_id])
    posted_result = None
    for row in cursor:
        posted_result = {'id':row[DATASET_ID_COL],'job_id':row[DATASET_JOB_ID_COL],'result':row[DATASET_RESULT_COL]}
    db.close()
    return posted_result

def update_job(job_id,username,title,description):
    db = get_db()
    db.execute("update jobs set username = ?, title = ?, description = ? where id = ?",[username,title,description,job_id])
    db.commit()
    db.close()

def update_shader(job_id,shader):
    db = get_db()
    db.execute("update shaders set shader = ? where job_id = ?",[shader,job_id])
    db.commit()
    db.close()

def update_dataset(job_id,dataset_id,data):
    db = get_db()
    db.execute("update datasets set data = ?, status = ? where id = ? and job_id = ?",data,"not allocated",dataset_id,job_id)
    db.commit()
    db.close()

def update_result(job_id,dataset_id,result):
    db = get_db()
    db.execute("update datasets set result = ? where job_id = ? and id = ?",[result,job_id,dataset_id])
    db.commit()
    db.close()

def delete_job(job_id):
    db = get_db()
    db.execute("delete from shaders where job_id = ?",[job_id])
    db.execute("delete from datasets where job_id = ?",[job_id])
    db.execute("delete from jobs where id = ?", [job_id])
    db.commit()
    db.close()

def delete_dataset_by_id(job_id,dataset_id):
    db = get_db()
    db.execute("delete from datasets where job_id = ? and id = ?",[job_id,dataset_id])
    db.commit()
    db.close()


if __name__ == "__main__":
    print ("this is an sqlite db interface\nimport this file to use it")


