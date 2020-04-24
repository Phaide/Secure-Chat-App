import os
import shelve
import markdown
import base64

# Documentation : https://pycryptodome.readthedocs.io/en/latest/
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

import mysql.connector

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

def log(data):
    with open("log.txt", "a") as log:
        log.write(str(data) + "\n")

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

        parser.add_argument("pubkey_n", required = True)
        parser.add_argument("pubkey_e", required = True)
        parser.add_argument("address", required = True)
        parser.add_argument("hash", required = True)
        parser.add_argument("sig", required = True)

        args = parser.parse_args()

        # Load the key, and verify it is correct. Returns HTTP 400 Bad request upon error
        try:
            try:
                nodePubkey = RSA.construct((int(args["pubkey_n"]), int(args["pubkey_e"])), True)
            except ValueError:
                raise ValueError
            except Exception as e:
            if (nodePubkey.size_in_bits() != 4096):
                raise ValueError
        except ValueError:
            return {"message": "Invalid public key", "data": args}, 400

        # Create a new hash object of the request's pubkey
        h = SHA256.new("".join([str(nodePubkey.n), str(nodePubkey.e)]).encode("utf-8"))

        # Verify authentication. Returns HTTP 401 Unauthorized on error.
        try:
            if (h.hexdigest() == args["hash"]):
                pkcs1_15.new(nodePubkey).verify(h, base64.b64decode(args["sig"].encode("utf-8")))
            else:
                raise ValueError
        except ValueError:
            return {"message": "Authentication failed", "data": args}, 401

        args.pop("sig")

        shelf = get_db()
        shelf[args["pubkey_n"]] = args

        return {"message": "Node registered", "data": args}, 201


api.add_resource(NodesList, "/nodes")
