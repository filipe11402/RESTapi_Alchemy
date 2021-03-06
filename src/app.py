from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import RegisterUser
from resources.item import Item, ItemList


app = Flask(__name__)
app.secret_key = 'filipe'
jwt = JWT(app, authenticate, identity)
api = Api(app)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(RegisterUser, '/register')


if __name__ == '__main__':
    app.run(debug=True)