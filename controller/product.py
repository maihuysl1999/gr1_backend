from random import random, randrange
from flask import request, jsonify
import json

from toolz.itertoolz import cons, get, random_sample
from controller.Get import Handler1 as handler1
import common.Constant as constant
from bson.objectid import ObjectId
from bagri_sdk.py_handler import Handler as handler
contract_address = '0xd27b8e5Dffa5034cB3C8C2c682DC0cAE63E14613'
def getListProduct(_userid, mongo):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        role = getInfodUserById["role"]

        items = []
        if(role == constant.Constants["LienGroup"]) :
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
def getproduct(_userid, mongo):
    try:
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        role = getInfodUserById["role"]
        getContractByAddressContract = product_collection.find_one({"address_contract" : ObjectId(contract_address)})
        data_info = json.load(getContractByAddressContract)["data_info"]
        print(data_info)
        resultgetDat = handler.get_soil(data_info["soil_ids"])
        resultgetNuoc = handler.get_water(data_info["water_ids"])
        resultgetGiong = handler.get_genus(data_info["genus_ids"])
        resultgetInfo = ""
        resInfo = {
            "name": "Thong tin mua vu",
            "data": [
                {
                    "name": "Thoi gian",
                    "data": data_info[0]
                },
                {
                    "name": "Ten",
                    "data": data_info[1]
                },
                {
                    "name": "Dia Diem",
                    "data": data_info[2]
                },
                {
                    "name": "Dien Tich ",
                    "data": data_info[3]
                }
            ]
        }
        resDat = {
            "name": "Thong tin ve Dat",
            "data": [
                {
                    "name": "Thoi gian",
                    "data": resultgetDat[0]
                },
                {
                    "name": "Loai Dat",
                    "data": resultgetDat[1]
                },
                {
                    "name": "Do Ph ",
                    "data": resultgetDat[2]
                },
                {
                    "name": "Vi Tri ",
                    "data": resultgetDat[3]
                },
                {
                    "name": "Mieu ta ",
                    "data": resultgetDat[4]
                }
            ]
        }
        resNuoc = {
            "name": "Thong tin ve Nuoc",
            "data": [
                {
                    "name": "Thoi gian",
                    "data": resultgetNuoc[0]
                },
                {
                    "name": "Loai Nuoc",
                    "data": resultgetNuoc[1]
                },
                {
                    "name": "Do Ph ",
                    "data": resultgetNuoc[2]
                },
                {
                    "name": "Vi Tri ",
                    "data": resultgetNuoc[3]
                },
                {
                    "name": "Mieu ta ",
                    "data": resultgetNuoc[4]
                }
            ]
        }
        resGiong = {
            "name": "Thong tin ve Giong",
            "data": [
                {
                    "name": "Thoi gian",
                    "data": resultgetGiong[0]
                },
                {
                    "name": "Loai Giong",
                    "data": resultgetGiong[1]
                },
                {
                    "name": "Nguon Goc",
                    "data": resultgetGiong[2]
                },
                {
                    "name": "Mieu ta ",
                    "data": resultgetGiong[3]
                }
            ]
        }
        resLichsu = {
            "name": "Cau hinh ghi nhat ky",
            "data": [
                {
                    "name": "Thoi gian",
                    "data": None
                },
                {
                    "name": " Hanh Dong",
                    "data": None
                },
                {
                    "name": "Mieu ta",
                    "data": None
                }
            ]
        }
        resThem = {
            "name": "Thong tin them",
            "data": getContractByAddressContract["data"]
        }
        getVerifyContract = handler1.getVerifySmartcontract(contract_address)
        getMsg = mongo.db.find_one({"address_contract" : ObjectId(contract_address)})
        if (getMsg):
            status_msg = getMsg["status"]
        else :
            status_msg = None
        return jsonify({
            "status": 200,
            "resp_info": resInfo,
            "resp_dat": resDat,
            "resp_giong": resGiong,
            "resp_nuoc": resNuoc,
            "resp_them": resThem,
            "resp_history": resLichsu,
            "verify_contract": getVerifyContract,
            "status_msg": status_msg,
      })
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )
def getHistory(_userid, mongo):
    try:
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        role = getInfodUserById["role"]
        getContractByAddressContract = product_collection.find_one({"address_contract" : ObjectId(contract_address)})
        getCount = handler1.getCount(contract_address, _userid)
        item = []
        for history_id in range(0,int(getCount,base=10)):
            gethistory = handler.get_history(history_id)
            data = {
                "time": gethistory[0],
                "action_name":gethistory[1],
                "key_qrcode": gethistory[2],
                "description":gethistory[3]
            }
            item.append(data)
        getCountCustom = handler1.getCountCustom(contract_address)
        itemAdd = []
        Name = []  
        for i in range(0,len(getContractByAddressContract)):
            Name.append(getContractByAddressContract[i]["name"])
        for i in range(0,int(getCountCustom)) :
            getDataCustom = handler1.getDataCustom(_userid)
            dataAdd = []
            for j in range(0,len(Name)):
                value = {
                    "name": Name[j],
                    "data": getDataCustom[j]
                }
                dataAdd.append(value)
            itemAdd.append(dataAdd)
        return jsonify(status = 200, data = item, itemsAdd = itemAdd )
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )    
def getqrcode(_userid, mongo):
    try:
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        role = getInfodUserById["role"]
        getContractByAddressContract = product_collection.find_one({"address_contract" : ObjectId(contract_address)})
        if (role != constant["Group"]):
            return jsonify(status = 500, msg = "Bạn không có quyền get Qr code")
        resultAllGetKeyQrCode = handler1.getKeyQrCode(contract_address)
        if (resultAllGetKeyQrCode == None):
            return jsonify(status = 200, items = None)
        items = []
        for i in range(0,len(resultAllGetKeyQrCode)):
            resultQrcode = handler1.getQrCode(contract_address, resultAllGetKeyQrCode[i])
            data = {
                "time": resultQrcode[0],
                "action_name": resultQrcode[1],
                "description": resultQrcode[2],
                "key": resultQrcode[3]
            }
            items.append(data)
        return jsonify(status = 200, items = items)
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )
def getListMsg(_userid, mongo):
    try:
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        msgdb = mongo.db.msg 
        role = getInfodUserById["role"]
        getContractByAddressContract = product_collection.find_one({"address_contract" : ObjectId(contract_address)})
        if (getInfodUserById["role"] != constant["LienGroup"]):
            return jsonify(status = 500, msg = "Bạn không có quyền , chỉ liên nhóm mới có thể get msg")
        items = []
        getAllMsg = msgdb.find({"user_id_lien_group" : ObjectId(_userid)})
        for i in range(0,len(getAllMsg)):
            get_user = user_collection.find_one(getAllMsg[i].user_id)
            getAllMsg[i].user_id = get_user["email"]
            items.append(getAllMsg[i])
        print(items)
        return jsonify(status = 200, items = items)
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )        
def getMsgActionForFarmer(_userid, mongo):
    try:
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        msgdb = mongo.db.msg 
        role = getInfodUserById["role"]
        getContractByAddressContract = product_collection.find_one({"address_contract" : ObjectId(contract_address)})
        msgaction = mongo.db.msgaction
        get_msg_action = msgaction.find({"user_id_household": ObjectId(_userid), "address_contract": contract_address })
        return jsonify(status = 200, items = get_msg_action)
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )    
import math
from datetime import datetime
def setQrCode(data, _userid,mongo):
    try:
        actionName = data["action_name"]
        description = data["description"]
        _keyQrcode = math.floor(random() * (1000000000 - 1) + 1)
        msgaction = mongo.db.msgaction
        user_collection = mongo.db.users
        product_collection = mongo.db.product
        househoulds_collection = mongo.db.contracts
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(_userid)})
        getContractByAddressContract = product_collection.find_one({"address_contract" : ObjectId(contract_address)})
        role = getInfodUserById["role"]
        now = datetime.now()
        timeNow = now.strftime("%d/%m/%Y %H:%M:%S")
        if (role != constant["Group"]):
            return jsonify(status=500, msg="Ban khong co quyen tao Qr code")
        getAllHousehold = househoulds_collection.find({"parent_group_id": ObjectId(_userid), "contract_id": getContractByAddressContract["_id"]})
        for i in range(0,len(getAllHousehold)):
            data_insert = {
                'user_id': _userid,
                'user_id_household': getAllHousehold[i].user_id,
                'status': 0,
                'address_contract': contract_address,
                'key_action': _keyQrcode,
                'data':""
            }
        msgaction.insert_one(data_insert)
        setQrCode = handler1.set_QrCode(actionName,description,_keyQrcode,timeNow)
        return jsonify(status = 200, msg = "Tao Qr code thanh cong.", tx = setQrCode)
    except Exception as e:
        print (e)
        return jsonify(status = 500, 
                error = e )    


