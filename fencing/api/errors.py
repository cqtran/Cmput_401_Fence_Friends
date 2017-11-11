from database.db import dbSession, init_db

from flask.json import jsonify

# Source: https://stackoverflow.com/questions/21294889/how-to-get-access-to-error-message-from-abort-command-when-using-custom-error-ha
# A helper function for creating error responses
def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response
