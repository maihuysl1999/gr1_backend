from os import error
import uuid
from bson.objectid import ObjectId

from flask.json import jsonify

import datetime

def setBagri(data,userid, mongo, handler):
    try: 
        user_collection = mongo.db.users
        result = user_collection.find_one({"_id" : ObjectId(userid)})
        if not result or result["role"] != '1': 
            return jsonify(status = 500, msg = "you are not admin")
        bagri_collection = mongo.db.bagris
        arr_product = []
        id = uuid.uuid1()
        time_end = ""
        if not "description" in data : 
            description = ""
        else :
            description = data["description"]
        result = handler.create_bagri(str(id), data["name"],data["time_start"], time_end,description, arr_product)
        print(result)
        bagri_collection.insert({
            "id" : str(id),
            "name": data["name"],
            "user_id" : ObjectId(userid)        
        })
        return jsonify(status = 200, msg= "thanh cong")

    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def setProduct(product_id, userid, data, mongo, handler ):
    try: 
        group_collection = mongo.db.groups
        products_collection = mongo.db.products
        result = group_collection.find_one({"user_id" : ObjectId(userid)})
        if not result : 
            return jsonify(status =  500, msg =  "Bạn không phải là quản lý của group nào")
        Info = data["dataInfo"]
        now = datetime.datetime.now()
        arr_action = []
        result1 = handler.create_product(product_id, Info[1], Info[3], Info[2], "", "0", str(now), [], [], [], arr_action,result["id_bagri"])
        print(result1)
        filter = { 'product_id': product_id }
        
        # Values to be updated.
        newvalues = { "$set": { 'address_contract': result1 } } 
        
        # Using update_one() method for single updation.
        products_collection.update_one(filter, newvalues) 
        return jsonify (status =  200)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)
