
COMMUNICATION HANDLER
    url: /jobs
        GET:
            get list of jobs

        POST:
            post new job

    url: /jobs/<id>
        GET:
            get specific job info

        PUT:
            update job info

        DELETE:
            delete job

    url: /jobs/<id>/shader
        GET:
            get job associated shader

        PUT:
            update job associated shader

    url: /jobs/<id>/datasets
        GET:
            get a list of job associated datasets

        POST:
            add a dataset to the job
        
    url: /jobs/<id>/datasets/<id>
        GET:
            get a dataset to be run by the job

        PUT:
            update dataset

        DELETE:
            deletes the associated dataset

    url: /jobs/<id>/datasets/<id>/results
        GET:
            request de dataset results

        POST:
            post the resulting data

        PUT:
            update results




