# instead of having dictionaries as in security.py we can create a suer class

# to store the data, and we can just creat e a ause robject that is going to be essentially the same thing as the dict
#

import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be left blank! ')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank! ')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists!"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
