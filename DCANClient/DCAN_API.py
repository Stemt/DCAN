PROTOCOL = "http"

USERS_URI = "/users"
USERS_ID_URI = "/users/{user_id}"
USERS_NAME_URI = "/users/{username}"

JOBS_URI = "/jobs"
JOB_ID_URI = "/jobs/{job_id}"
JOB_ID_SHADER_URI = "/jobs/{job_id}/shader"
JOB_ID_DATASET_INFO_URI = "/jobs/{job_id}/datasets" #needs to refactored to JOB_ID_DATASETS_URI
JOB_ID_DATASET_ID_URI = "/jobs/{job_id}/datasets/{dataset_id}"
JOB_ID_DATASET_ID_RESULTS_URI = "/jobs/{job_id}/datasets/{dataset_id}/results"

url_template = "{protocol}://{server_address}{uri}"