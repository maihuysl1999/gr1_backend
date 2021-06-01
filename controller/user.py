from flask import request, jsonify
import json
import helpers.jwt_helper as jwtHelper
import common.Constant as constant

def sign_up( _name, _email, _password, _role, mongo):
    user_collection = mongo.db.users
    checkEmail = user_collection.find_one({"email": _email })
    if checkEmail : 
        print("false")
        return jsonify(status = 500, 
            msg = "Email already exists ")
    user_collection.insert({
        "name": _name,
        "email": _email,
        "password": _password,
        "role": _role,
        "address": "0xe4680B5B373b9353AF87De622a6E410E067a25c9",
        "private_key":
          "ef0be3ad9cf6ab09b1aaca99e1880546e4ca82e159a590291d0ec67e5929d0cf",
      })
    print("true")
    return jsonify(status = 200,
        message = "thanh cong" )
def login(_email, _password, mongo):
    try:
        user_collection = mongo.db.users
        result = user_collection.find_one({"email": _email, "password": _password })
        if result :    
            temp = str(result["_id"])
            result["_id"] = temp
            accessToken = jwtHelper.generateToken(result["_id"],
                constant.Constants["ACCESS_TOKEN_SECRET"],
                constant.Constants["ACCESS_TOKEN_LIFE_RESET_PASSWORD"])
            return jsonify(status = 200, 
                msg = "thanh cong",
                user = result ,
                access_token =  accessToken)
        else: 
            return jsonify(status = 500, 
                msg = "login fail")
    except Exception as e:
        return jsonify(status = 500, 
                error = e )