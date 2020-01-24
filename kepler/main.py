from flask import Flask, request, jsonify
from app.users.sign_in import sign_in_service
from app.users.sign_up import sign_up_service
from app.users.update_profile import edit_profile
from app.users.update_password import edit_password
from app.users.remove_user import delete_user

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


# Editing user profile
@app.route('/update_profile', methods=['POST'])
def update_profile():
    try:
        request_data = request.get_json()
        data = edit_profile(request_data['user_id'], request_data['name'], request_data['email'], request_data['phone'],
                            request_data['address'])
        return jsonify(data)
    except Exception as e:
        traceback.print_exc()
        return "Error occurred: ", str(e)


# Update user password
@app.route('/update_password', methods=['POST'])
def update_password():
    try:
        request_data = request.get_json()
        data = edit_password(request_data['user_id'], request_data['password'])
        return jsonify(data)
    except Exception as e:
        return "Error occurred: ", str(e)


# Delete User profile
@app.route('/remove_profile', methods=['POST'])
def remove_profile():
    try:
        request_data = request.get_json()
        data = delete_user(request_data['user_id'])
        return jsonify(data)
    except Exception as e:
        return "Error occurred: ", str(e)


if __name__ == '__main__':
    app.run(debug=True)
