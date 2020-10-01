import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This Field Cannot Be Left Blank!'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='This Field Cannot Be Left Blank!'
    )

    def post(self):

        data = UserRegister.parser.parse_args()
        user_already_exists = UserModel.find_by_username(data['username'])

        if user_already_exists:
            return { "message": "A User With That Username Already Exists." }, 400

        user = UserModel(**data)
        user.save_to_db()

        return { "message": "User Created Successfully." }, 201
