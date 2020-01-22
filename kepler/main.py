from flask import Flask, request, jsonify
from kepler.app.users.sign_in import sign_in_service
from kepler.app.users.sign_up import sign_up_service
from kepler.service import es_db
import os
import traceback

app = Flask(__name__)


# Authenticator
@app.route('/sign_in', methods=['POST'])
def sign_in():
    try:
        request_data = request.get_json()
        email = request_data['email']
        password = request_data['password']

        data = sign_in_service(email, password)

        return jsonify(data)
    except Exception as e:
        traceback.print_exc()
        return "Error :", str(e)


# Creating a new user
@app.route('/sign_up', methods=['POST'])
def sign_up():
    try:
        request_data = request.get_json()
        data = sign_up_service(request_data['name'], request_data['email'], request_data['mobile'],
                               request_data['address'], request_data['password'])

        return jsonify(data)
    except Exception as e:
        traceback.print_exc()
        return "Error :", str(e)


if __name__ == '__main__':
    app.run(debug=True)
