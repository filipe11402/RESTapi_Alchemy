import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="You need to pass a username")
    parser.add_argument('password', type=str, required=True, help="You need to define a password")


    def post(self):
        data = RegisterUser.parser.parse_args()

        if UserModel.find_by_username(data['username']) is None:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "INSERT INTO users (id, username, password) VALUES (NULL, ?, ?)"
            cursor.execute(query, (data['username'], data['password'],))

            connection.commit()
            connection.close()

            return {'message': 'user created successfully'}, 201
        
        return {'message': 'That user already exists'}, 400