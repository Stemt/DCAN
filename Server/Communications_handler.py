import base64

from flask import *
import Database_interface as db
app = Flask(__name__)

#TODO add resource acces based on account privileges
#NOTE currently the API allows for bypassing the account restrictions
# this is a major design flaw and requires redesign of the API

#untested
@app.route('/users', methods=['GET'])
def get_users():
    return make_response(jsonify(db.get_users()))

#untested
@app.route('/users/<string:username>', methods=['GET'])
def get_user_by_name(username):
    return make_response(jsonify(db.get_user_by_name(username)))

#untested
@app.route('/users', methods=['POST'])
def create_user():
    content = request.json
    print(content)
    created_user = db.create_user(content['username'],content['password'])
    return make_response(jsonify(created_user))

#untested
@app.route('/jobs', methods=['GET'])
def get_jobs():
    return make_response(jsonify(db.get_jobs()))

#untested
@app.route('/jobs', methods=['POST'])
def post_job():
    content = request.json
    print(content)
    created_job = db.create_job(content['username'],content['title'],content['description'])
    return make_response(jsonify(created_job))

#untested
@app.route('/jobs/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    return make_response(jsonify(db.get_job_by_id(job_id)))

#untested
@app.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db.delete_job(job_id)

#untested
@app.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job_by_id(job_id):
    content = request.json
    db.update_job(job_id,content['username'],content['title'],content['description'])

#untested
@app.route('/jobs/<int:job_id>/shader', methods=['GET'])
def get_shader(job_id):
    shader = db.get_shader(job_id)
    print(shader)
    return make_response(jsonify(shader))

#untested
@app.route('/jobs/<int:job_id>/shader', methods=['POST'])
def create_shader(job_id):
    content = request.json
    print(content)
    shader = content['shader']# base64.b64decode(content['shader'])
    created_shader = db.create_shader(job_id,shader)
    return make_response(jsonify({'id':created_shader['id']}))

#untested
@app.route('/jobs/<int:job_id>/shader', methods=['PUT'])
def update_shader(job_id):
    content = request.json
    db.update_shader(job_id,content['data'])

#untested
@app.route('/jobs/<int:job_id>/datasets', methods=['GET'])
def get_datasets(job_id):
    return make_response(jsonify(db.get_datasets(job_id)))

#untested
@app.route('/jobs/<int:job_id>/datasets', methods=['POST'])
def create_dataset(job_id):
    content = request.json
    created_dataset = db.create_dataset(job_id,content['data'])
    return make_response(jsonify(created_dataset))

#untested
@app.route('/jobs/<int:job_id>/datasets/<int:dataset_id>', methods=['GET'])
def get_dataset_by_id(job_id,dataset_id):
    return make_response(jsonify(db.get_dataset_by_id(job_id,dataset_id)))

#untested
@app.route('/jobs/<int:job_id>/datasets/<int:dataset_id>', methods=['PUT'])
def update_dataset_by_id(job_id,dataset_id):
    content = request.json
    db.update_dataset(job_id,dataset_id,content['data'])

#untested
@app.route('/jobs/<int:job_id>/datasets/<int:dataset_id>', methods=['DELETE'])
def delete_dataset_by_id(job_id,dataset_id):
    db.delete_dataset_by_id(job_id,dataset_id)

#untested
@app.route('/jobs/<int:job_id>/datasets/<int:dataset_id>/results', methods=['GET'])
def get_dataset_by_id_results(job_id,dataset_id):
    return make_response(jsonify(db.get_dataset_by_id_results(job_id,dataset_id)))

#untested
#TODO not implemented
@app.route('/jobs/<int:job_id>/datasets/<int:dataset_id>/results', methods=['POST'])
def post_result(job_id,dataset_id):
    content =  request.json
    return make_response(jsonify(db.post_result(job_id,dataset_id,content['results'])))

#untested
@app.route('/jobs/<int:job_id>/datasets/<int:dataset_id>/results', methods=['PUT'])
def update_result(job_id,dataset_id):
    content = request.json
    db.post_result(job_id,dataset_id,content['results'])


if __name__ == '__main__':
    app.run(debug=True)