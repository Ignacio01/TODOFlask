from flask import jsonify, make_response
from app import app

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
