from flask import jsonify, abort, make_response, request
# app defined in the __init__
from app import app, db
from app.models import Task

"""
    Currently not implemented the database.
    Using a list with dictionary, but should use a database.
    Next step would be creating a database.
"""


@app.route('/', methods=['GET'])
def get_task():
    """
    :return:
        all the tasks in the list
    """
    tasks_db = Task.query.all()
    output = []

    if len(tasks_db) == 0:
        return jsonify({'lists': 'No tasks to be done'})

    for task in tasks_db:
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['done'] = task.done
        output.append(task_data)

    return jsonify({'lists': output})


@app.route('/<int:task_id>', methods=['GET'])
def get_individual_task(task_id):
    """
    :param task_id:
        The task id is passed with the route.
    :return:
        Returns json with the task if found, else abort would be executed.
    """
    task = Task.query.get(task_id)

    if task is None:
        abort(404)

    output = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done
    }

    return jsonify({'task': output})


@app.route('/', methods=['POST'])
def create_task():
    """
    To test the creation using curl
    curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book", "description": "Reading is fun"}'
    http://localhost:5000/
    :return:
    """
    tasks_db = Task.query.all()
    tasks = []

    for task in tasks_db:
        dict_task = {}
        dict_task['id'] = task.id
        dict_task['title'] = task.title
        dict_task['description'] = task.description
        dict_task['done'] = task.done
        tasks.append(dict_task)

    data_received = request.json

    if not data_received or not 'title' in data_received:
        abort(400)

    # Created the object task
    task_db = Task()
    task_db.title = data_received['title']
    task_db.description = data_received['description']
    task_db.done = False

    db.session.add(task_db)
    db.session.commit()

    # Converting the object task to a dictionary
    task_dict = {
        'id': task_db.id,
        'title': task_db.title,
        'description': task_db.description,
        'done': task_db.done
    }

    tasks.append(task_dict)

    return jsonify({'tasks': tasks}), 201


@app.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/2
    :param task_id:
    :return:
    """
    task = [task for task in tasks if task['id'] == task_id]

    # Validate that the fields to be updated are not incorrect
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    # unicode not working
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400)

    # Update the values in the array task
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])

    return jsonify({'task': task[0]})


@app.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """

    :param task_id:
    :return:
    """
    task = [task for task in tasks if task['id'] == task_id]

    if len(task) == 0:
        abort(404)

    tasks.remove(task[0])
    return jsonify({'tasks': tasks})


@app.errorhandler(404)
def not_found(error):
    """
    Handle the exception when something is not found (404)
    :param error:
    :return:
        Json with error message.

    """
    return make_response(jsonify({'error': 'Task not Found'}))


@app.errorhandler(400)
def incorrect_data(error):
    return make_response(jsonify({'error': 'Incorrect Parameters'}))
