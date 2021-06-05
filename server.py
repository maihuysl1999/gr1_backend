import flask 
from flask import request, jsonify
from flask_pymongo import PyMongo
from werkzeug.datastructures import auth_property
from werkzeug.wrappers import response


import controller.user as user
import controller.product as product

import controller.setblockchain as setblc

# some_file.py
import sys
# # insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'D:\\GR1\\bagri_sdk')

import py_handler
from py_handler import Handler

handler = Handler()

 

import re

import middlewares.AuthMiddleware as middleWare
 
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

@app.route('/v0/login', methods=['POST'])
def login():
    data = request.get_json()   
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )    
    if not "password" in data :
        return jsonify(status = 500, 
        msg = "Please enter a valid password." )
    email = data ["email"]
    password = data["password"]
    return user.login(email, password, mongo)

#quan ly lien nhom: role = 1
#in ra danh sach cac nhom
@app.route('/v0/get_list_group', methods=['POST'])
def get_list_group():
    try : 
        data = request.get_json()
        print(data)
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.getListGroup(data, auth, mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
#them nhom moi
@app.route('/v0/add_groups', methods=['POST'])
def add_groups():
    data = request.get_json()
    print(data)
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.addGroup(data, auth, mongo)
        # print(auth)
        # return jsonify(status = 500, 
        #     msg = "Please enter a valid password." )
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
#tao mua vu moi
@app.route('/v0/create_bgri', methods=['POST'])
def create_bgri():  
    data = request.get_json()
    print(data)
    if (not "time_start" in data) or (not "name" in data):
        return jsonify(status = 500, 
        msg = "Please enter a valid time start or name" )
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return setblc.setBagri(data, auth, mongo, handler)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
    # return jsonify(success = True,
    #     message = "thanh cong",
    #     id_bagri= str(id) )

@app.route('/v0/get_list_bgri', methods=['GET'])
def get_list_bgri():
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.getListBgri(auth, mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )



#quan ly nhom : role = 2 
@app.route('/v0/add_households', methods=['POST'])
def add_households():
    data = request.get_json()
    if (not "email" in data) or (not re.search(regex, data["email"])) :
        return jsonify(status = 500, 
        msg = "Please enter a valid email" )
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return user.addHouseHold(data, mongo)
        # print(auth)
        # return jsonify(status = 500, 
        #     msg = "Please enter a valid password." )
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )
# quan ly lien nhom, quan ly nhom, ho dan : role = 1, 2, 3
@app.route('/v0/get_list_product', methods=['GET'])
def getListProduct():
    try : 
        auth = middleWare.isAuth(request, mongo)
        if isinstance(auth, dict) :
            return jsonify(status = auth["status"], 
                msg = auth["msg"])
        return product.getListProduct(auth, mongo)
    except Exception as e:
        print(e)
        return jsonify(status = 500, 
                error = e )




app.run()