from os import error
import uuid
from bson.objectid import ObjectId

from flask.json import jsonify

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
