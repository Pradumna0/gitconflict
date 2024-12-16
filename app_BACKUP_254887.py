#Changes here 
#new cahnges
<<<<<<< HEAD
#Another change from master branch
=======
#Another one file from newBranch
>>>>>>> newBranch
#This changes From Master branch
#Git merge with cli
from flask import Flask, jsonify, request
import redis
import json
import uuid
from dotenv import load_dotenv
import os
from werkzeug.exceptions import BadRequest     # for raise the error if req. is unappropriated

load_dotenv()
app = Flask(__name__)

# Redis configuration
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
# print(REDIS_PASSWORD)
# REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
# REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Connect to Redis and check if the password is correct
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)  #, password=REDIS_PASSWORD
    r.ping()
    print("Successfully connected to Redis with the correct password.")
except redis.exceptions.AuthenticationError:
    print("Error: Incorrect Redis password.")
    exit(1)
except redis.exceptions.ConnectionError as e:    #if redis-server unavilable
    print(f"Error: Could not connect to Redis. {e}")
    exit(1)

# Helper functions
def get_task(task_id):
    task = r.get(task_id)
    if task:
        return json.loads(task)     #converts JSON to python dic. and return
    return None

def validate_task_data(task_data):
    if not isinstance(task_data, dict):
        raise BadRequest("Invalid input: Task data must be a JSON object.")
    if 'title' not in task_data or not isinstance(task_data['title'], str) or not task_data['title'].strip():
        raise BadRequest("Invalid input: 'title' is required and must be a non-empty string.")
    if 'description' in task_data and not isinstance(task_data['description'], str):
        raise BadRequest("Invalid input: 'description' must be a string.")
    return task_data

# Endpoints
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = [json.loads(r.get(key)) for key in r.keys()]      
        return jsonify(tasks), 200             #return the list of task in JSON format
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve tasks: {str(e)}'}), 500

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    try:
        task = get_task(task_id)
        if task:
            return jsonify(task), 200
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve task: {str(e)}'}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_data = request.json
        task_data = validate_task_data(task_data)

        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'title': task_data['title'],
            'description': task_data.get('description', ''),
            'status': 'Pending'
        }
        r.set(task_id, json.dumps(task))    #serealized task as a JSON string
        return jsonify(task), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to create task: {str(e)}'}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = get_task(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        task_data = request.json
        if not isinstance(task_data, dict):
            raise BadRequest("Invalid input: Task data must be a JSON object.")

        task['title'] = task_data.get('title', task['title'])
        task['description'] = task_data.get('description', task['description'])
        task['status'] = task_data.get('status', task['status'])

        r.set(task_id, json.dumps(task))
        return jsonify(task), 200
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to update task: {str(e)}'}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        if r.delete(task_id):
            return jsonify({'message': 'Task deleted'}), 200
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete task: {str(e)}'}), 500

@app.route('/tasks/<task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    try:
        task = get_task(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        if 'status' not in request.json or not isinstance(request.json['status'], str):
            raise BadRequest("Invalid input: 'status' is required and must be a string.")

        task['status'] = request.json['status']
        r.set(task_id, json.dumps(task))
        return jsonify(task), 200
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to update task status: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True)



# curl -X GET http://localhost:8000/tasks
# curl -X GET http://localhost:8000/tasks/<task_id>
# curl -X POST -H "Content-Type: application/json" -d '{"title": "My Task", "description": "Description of the task"}' http://localhost:8000/tasks
# curl -X PUT -H "Content-Type: application/json" -d '{"title": "Updated Task Title", "status": "Completed"}' http://localhost:8000/tasks/<task_id>
# curl -X DELETE http://localhost:8000/tasks/<task_id>
# curl -X PATCH -H "Content-Type: application/json" -d '{"status": "In Progress"}' http://localhost:8000/tasks/<task_id>/status




# curl -X PUT -H "Content-Type: application/json" -d 'Invalid data' http://localhost:8000/tasks/<task_id>
# curl -X PATCH -H "Content-Type: application/json" -d '{}' http://localhost:8000/tasks/<task_id>/status
# curl -X PATCH -H "Content-Type: application/json" -d '{"status": 123}' http://localhost:8000/tasks/<task_id>/status
# curl -X GET http://localhost:8000/tasks/nonexistent-id
# curl -X DELETE http://localhost:8000/tasks/nonexistent-id
# curl -X POST -H "Content-Type: application/json" -d '{"title": "Bad JSON}' http://localhost:8000/tasks



# https://chatgpt.com/share/6735c8e4-31a4-8001-8ecf-45a0048c938c







# from flask import Flask, jsonify, request
# import redis
# import json
# import uuid
# from dotenv import load_dotenv
# import os     #Access the environment variable

# load_dotenv()
# app = Flask(__name__)  #Initialize the falsk app

# # Redis configuration
# REDIS_PASSWORD = (os.getenv('REDIS_PASSWORD'))
# print(REDIS_PASSWORD)
# # REDIS_PASSWORD = "111" 
# # REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
# # REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
# # REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# # Connect to Redis and check if the password is correct
# try:
#     r = redis.Redis(host='redis', port=6379, password=REDIS_PASSWORD, decode_responses=True)
#     r.ping()  # This will check if the Redis server is reachable and the password is correct
#     print("Successfully connected to Redis with the correct password.")
# except redis.exceptions.AuthenticationError:
#     print("Error: Incorrect Redis password.")
#     exit(1)  # Exit the program if the password is incorrect

# # Task Model 
# def get_task(task_id):    #Helper function to retrive the task from Redis by task_id.
#     task = r.get(task_id)
#     if task:
#         return json.loads(task)   #Return deserialized Json data which means CONVERT JSON String to Python dictionary 
#     return None

# # Endpoints
# @app.route('/tasks', methods=['GET'])  #Define endpoint that listen for GET req. at the /task URL. Retrive data from the server
# def get_tasks():
#     tasks = []  
#     for key in r.keys():
#         tasks.append(json.loads(r.get(key)))
#     return jsonify(tasks), 200                   # Return a list of task as a JSON Response

# @app.route('/tasks/<task_id>', methods=['GET'])     
# def get_task_by_id(task_id):
#     task = get_task(task_id)
#     if task:
#         return jsonify(task), 200    # Return a task as a JSON Response
#     return jsonify({'error': 'Task not found'}), 404

# @app.route('/tasks', methods=['POST'])      #When a POST request is made to this endppoint, the craete task function is executed
# def create_task():                           #Create a New resource in the server
#     task_data = request.json            #Extract task data from request.json
#     task_id = str(uuid.uuid4())           #create a new task using a uuid.uuid4()  
#                                            #str() -> change object to the string
#     task = {
#         'id': task_id,
#         'title': task_data['title'],
#         'description': task_data.get('description', ''),
#         'status': 'Pending'
#     }
#     r.set(task_id, json.dumps(task))      #serialize the task dictionary to json string before storing in the Redis
#     return jsonify(task), 201               # Return the newly created task 

# @app.route('/tasks/<task_id>', methods=['PUT'])     #Define endpoint that listen for PUT requests at /tasks/<task_id>
# def update_task(task_id):                           #update the task data using task_id
#     task = get_task(task_id)
#     if not task:
#         return jsonify({'error': 'Task not found'}), 404

#     task_data = request.json
#     task['title'] = task_data.get('title', task['title'])
#     task['description'] = task_data.get('description', task['description'])
#     task['status'] = task_data.get('status', task['status'])

#     r.set(task_id, json.dumps(task))     #Dictionary to JSON 
#     return jsonify(task), 200   

# @app.route('/tasks/<task_id>', methods=['DELETE'])  #Delete a Task using Task Id
# def delete_task(task_id):
#     if r.delete(task_id):
#         return jsonify({'message': 'Task deleted'}), 200
#     return jsonify({'error': 'Task not found'}), 404

# @app.route('/tasks/<task_id>/status', methods=['PATCH'])    #Define endpoint that listen for PATCH requests at /tasks/<task_id>  
#                                                             #Updates the status of a specific task using a PATCH request
# def update_task_status(task_id):                            # Update part of an existing Resources
#     task = get_task(task_id)
#     if not task:
#         return jsonify({'error': 'Task not found'}), 404

#     task['status'] = request.json['status']
#     r.set(task_id, json.dumps(task))
#     return jsonify(task), 200

# if __name__ == "__main__":    # Start the Flask app in debug mode
#     app.run(debug=True)       # Automatic code reloading and detailed error msg during development.