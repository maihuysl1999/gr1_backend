from re import DEBUG
from flask import request, jsonify
import json

import uuid
import datetime

import common.Constant as constant
from bson.objectid import ObjectId

import controller.setblockchain as setblc

def getListProduct(_userid, mongo):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        role = getInfodUserById["role"]

        items = []
        if(role == constant.Constants["LienGorup"]) :
            getContract = product_collection.find({"parent_id" :ObjectId(_userid)})
            for document in getContract: 
                temp = str(document["user_id"])
                document["user_id"] = temp
                temp = str(document["_id"])
                document["_id"] = temp
                temp = str(document["parent_id"])
                document["parent_id"] = temp
                items.append(document)
            return jsonify(status = 200, items = items)
        if(role == constant.Constants["Group"]):
            getContract = product_collection.find({"user_id" :ObjectId(_userid)})
            for document in getContract: 
                temp = str(document["user_id"])
                document["user_id"] = temp
                temp = str(document["_id"])
                document["_id"] = temp
                temp = str(document["parent_id"])
                document["parent_id"] = temp
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

def getVietGap():   
    try: 
        return jsonify(status = 200, data = constant.Constants["VietGap"])
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )

def createProduct(data,userid, mongo, handler ):
    try: 
        group_collection = mongo.db.groups
        products_collection = mongo.db.products
        result = group_collection.find_one({"user_id" : ObjectId(userid)})
        if not result : 
            return jsonify(status =  500, msg =  "Bạn không phải là quản lý của group nào")
        id = uuid.uuid1()
        now = datetime.datetime.now()
        info_product = {
            "product_id" : str(id),
            "address_contract" : "",
            "name": data["dataInfo"][1],
            "user_id": ObjectId(userid),
            "parent_id": result["parent_id"],
            "data_info": data["dataInfo"],
            "status": "false",
            "description": "",
            "createAt" : now,
        }
        products_collection.insert(info_product)
        setblc.setProduct(str(id),userid, data, mongo, handler)
        temp = str(info_product["user_id"])
        info_product["user_id"] = temp
        temp = str(info_product["parent_id"])
        info_product["parent_id"] = temp
        temp = str(info_product["_id"])
        info_product["_id"] = temp
        return jsonify (status =  200, result = info_product )
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)
