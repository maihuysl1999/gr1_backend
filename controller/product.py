from flask import request, jsonify
import json
import common.Constant as constant
from bson.objectid import ObjectId

def getListProduct(_userid, mongo):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        role = getInfodUserById["role"]

        items = []
        if(role == constant.Constants["LienGorup"]) :
            getContract = product_collection.find({"parent_id" :ObjectId(_userid)})
            for document in getContract: 
                items.append(document)
            return jsonify(status = 200, items = items)
        if(role == constant.Constants["Group"]):
            getContract = product_collection.find({"user_id" :ObjectId(_userid)})
            for document in getContract: 
                items.append(document)
            return jsonify(status = 200, items = items)
        if(role == constant.Constants["HouseHolds"]):
            getHouseHoldsByID = househoulds_collection.find({"user_id" :ObjectId(_userid)})
            for document in getHouseHoldsByID:
                getProduct = product_collection.find({"id": document["product_id"]})
                if getProduct :
                    items.append(getProduct)
            
            return jsonify(status = 200, items = items)
        return jsonify(status = 200, items = items)
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )


