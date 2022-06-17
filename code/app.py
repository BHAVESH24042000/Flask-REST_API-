from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Bhavesh'
api = Api(app)

jwt = JWT(app, authenticate, identity) # creates /auth endpoint

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':  # this is done so that app.run() runs only throught this file
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True