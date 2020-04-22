import os
import rsa
import shelve
import markdown
import base64

from Crypto.Hash import SHA3_512
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import mysql.connector

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

import keygen
keygen.main()

app = Flask(__name__)

api = Api(app)

def get_db():
    #db = mysql.connector.connect(
    #    host = 'localhost:3306',
    #    database = os.environ['MYSQL_DATABASE'],
    #    user = 'root',
    #    password = os.environ['MYSQL_ROOT_PASSWORD'])
    #cursor = db.cursor()
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("nodes.db")
    return db
    #return db, cursor

@app.teardown_appcontext
def teardown(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_public_key():
    import publickey
    return publickey.pk

def get_private_key():
    import privatekey
    return privatekey.pk

@app.route("/")
def index():
    """
    Present the documentation
    """
    # Open the README.md file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        # Read the content of the file ans convert it to HTML
        return markdown.markdown(markdown_file.read())


class NodesList(Resource):
    def get(self):
        shelf = get_db()
        #conn, cursor = get_db()

        keys = list(shelf.keys())

        return {"message": "Success", "data": [shelf[key] for key in keys]}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("pass", required = True)
        parser.add_argument("uuid", required = True)
        parser.add_argument("pubkey", required = True)
        parser.add_argument("address", required = True)
        parser.add_argument("port", required = True)

        args = parser.parse_args()

        privkey = RSA.construct(get_private_key(), True)

        for key in args:
            args[key] = PKCS1_OAEP.new(privkey, SHA3_512).decrypt(base64.b64decode(args[key].encode("utf-8")), privkey)

        shelf = get_db()
        shelf[args["uuid"]] = args

        return {"message": "Node registered", "data": args}, 201

class PublicKey(Resource):
    def get(self):
        return {"message": "Public key gathered", "data": get_public_key()}, 200


api.add_resource(NodesList, "/nodes")
api.add_resource(PublicKey, "/key")
