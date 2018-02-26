from flask import jsonify, abort, request
# app defined in the __init__
from app import app, db
from app.models import Task
from app.errors import not_found, incorrect_data


@app.route('/', methods=['GET'])
def get_task():
    """
    :return:
        All the tasks in the database
    """
    output = []

    tasks_db = Task.query.all()

    if len(tasks_db) == 0:
        return jsonify({'lists': 'No tasks to be done'})

    for task in tasks_db:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'done': task.done
        }
        output.append(task_data)

    return jsonify({'lists': output})


@app.route('/<int:task_id>', methods=['GET'])
def get_individual_task(task_id):
    """
    :param task_id:
        The task id is passed with the route.
    :return:
        Returns a json items if the task found otherwise abort 404 not found
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
    This method creates a new task. Validates that the title is not empty.
    :return:
        The list with all the previous tasks plus the new task.
    """

    # Retrieving the current values in the database to show all the tasks
    tasks_db = Task.query.all()
    tasks = []

    for task in tasks_db:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'done': task.done
        }
        tasks.append(task_data)

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
    task_data = {
        'id': task_db.id,
        'title': task_db.title,
        'description': task_db.description,
        'done': task_db.done
    }
    tasks.append(task_data)

    return jsonify({'tasks': tasks}), 201


@app.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Changes the values of a task, except for the id
    :param task_id:
    :return:
        Returns the task updated.
    """

    data = request.json

    # Validate that the fields to be updated are not incorrect
    if not data:
        abort(400)
    # unicode not working
    if 'title' in data and type(data['title']) != str:
        abort(400)
    if 'description' in data and type(data['description']) != str:
        abort(400)
    if 'done' in data and type(data['done']) != bool:
        abort(400)

    task = Task.query.get(task_id)

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.done = data.get('done', task.done)

    db.session.commit()

    return jsonify({'task': {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done
    }})


@app.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Removes a task from the database
    :param task_id:
    :return:
        Returns a confirmation message if the task has been deleted correctly.
    """
    task = Task.query.get(task_id)
    if task is None:
        abort(404)
    db.session.delete(task)
    db.session.commit()

    return jsonify({'tasks': "Task {} deleted correctly".format(task_id)})
