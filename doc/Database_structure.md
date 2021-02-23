Database tables:
    users:{
        username:<string>
        password_hash:<string>
    }

    jobs:{
        id:<int>
        user_id:<int>
        title:<string>
        description:<string>
        status:<string> ("not worked on","being worked on","done")
    }

    shaders:{
        id:<int>
        job_id:<int>
        shader:<string>
    }

    datasets:{
        id:<int>
        job_id:<int>
        data:<string>
        result:<string>
        status:<string>
    }