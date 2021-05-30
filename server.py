import flask 
from flask import request, jsonify
from flask_pymongo import PyMongo

import controller.user as user
import re
 
# Make a regular expression
# for validating an Email
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


app = flask.Flask(__name__)
#app.config["DEBUG"] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/bgri"
mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/v0/signup', methods=['POST'])
def register():    
    data = request.get_json()  
    print(data)  
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )    
    if not "password" in data :
        return jsonify(status = 500, 
        msg = "Please enter a valid password." )
    if not "role" in data :
        return jsonify(status = 500, 
        msg = "Please enter a valid role." )
    if not "name" in data :
        name = ""
    else :
        name = data["name"]
    email = data ["email"]
    password = data["password"]
    role = data["role"]
    return user.sign_up(name, email, password, role, mongo)

app.run()