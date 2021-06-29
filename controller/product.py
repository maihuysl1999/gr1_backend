from itertools import product
from logging import error
from re import A, DEBUG
from flask import request, jsonify
import json

import uuid
import datetime

import common.Constant as constant
from bson.objectid import ObjectId

import controller.setblockchain as setblc
import controller.getblockchain as getblc

def getListProduct(_userid, mongo):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        households_collection = mongo.db.households
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
        print(role)
        if(role == constant.Constants["HouseHolds"]):
            getHouseHoldsByID = households_collection.find({"user_id" :ObjectId(_userid)})
            for document in getHouseHoldsByID:
                print(document)
                getProduct = product_collection.find_one({"_id": document["product_id"]})
                if getProduct :
                    temp = str(getProduct["user_id"])
                    getProduct["user_id"] = temp
                    temp = str(getProduct["_id"])
                    getProduct["_id"] = temp
                    temp = str(getProduct["parent_id"])
                    getProduct["parent_id"] = temp
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
            "status": False,
            "description": "",
            "genus_id" : "",
            "water_id" : "",
            "soil_id" : "", 
            "createAt" : now,
        }
        products_collection.insert(info_product)
        setblc.initProduct(str(id),userid, data, mongo, handler)
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

def getProduct(tx_hash, userid, mongo, handler):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        msg_collection = mongo.db.msg
        getInfodUserById =  user_collection.find_one({"_id" : ObjectId(userid)})
        getProduct = product_collection.find_one({"address_contract" : tx_hash})
        data_info = getProduct["data_info"]
        resultGetSoild = handler.get_soil(getProduct["soil_id"])
        resultGetWater = handler.get_water(getProduct["water_id"])
        resultGetGenus = handler.get_genus(getProduct["genus_id"])

        respInfo = {
            "name": "Thông tin mùa vụ",
            "data": [
            {
                "name": "Tên",
                "data": data_info[0],
            },
            {
                "name": "Địa điểm",
                "data": data_info[1],
            },
            {
                "name": "Diện tích",
                "data": data_info[2],
            },
            ],
        }
        respDat = {
            "name": "Thông tin về đất",
            "data": [
            {
                "name": "Loại đất",
                "data": resultGetSoild[1],
            },
            {
                "name": "Độ Ph",
                "data": resultGetSoild[2],
            },
            {
                "name": "Vị trí",
                "data": resultGetSoild[3],
            },
            {
                "name": "Miêu tả",
                "data": resultGetSoild[4],
            },
            ],
        }
        respNuoc = {
            "name": "Thông tin về nguồn nước",
            "data": [
            {
                "name": "Nguồn gốc",
                "data": resultGetWater[1],
            },
            {
                "name": "Độ Ph",
                "data": resultGetWater[2],
            },
            {
                "name": "Vị trí",
                "data": resultGetWater[3],
            },
            {
                "name": "Miêu tả",
                "data": resultGetWater[4],
            },
            ],
        }

        respGiong = {
            "name": "Thông tin về giống cây",
            "data": [
            {
                "name": "Tên giống",
                "data": resultGetGenus[1],
            },
            {
                "name": "Nguồn gốc",
                "data": resultGetGenus[2],
            },
            {
                "name": "Miêu tả",
                "data": resultGetGenus[3],
            },
            ],
        }

        respHistory = {
            "name": "Cấu hình ghi nhật kí",
            "data": [
            {
                "name": "Thời gian",
                "data": "",
            },
            {
                "name": "Hành động",
                "data": "",
            },
            {
                "name": "Miêu tả",
                "data": "",
            },
            ],
        }
        getMsg = msg_collection.find_one({ "address_contract": tx_hash, "status" : 2})

        if not getMsg :
            getMsgReject = msg_collection.find_one({"address_contract" : tx_hash, "status" : 3})
            if getMsgReject: 
                status_msg = 3
            else: 
                status_msg = ""
        else :
            status_msg = getMsg["status"]
        return jsonify(
            status =  200,
            resp_info = respInfo,
            resp_dat = respDat,
            resp_giong = respGiong,
            resp_nuoc =  respNuoc,
            resp_history = respHistory,
            verify_contract = getProduct["status"],
            status_msg = status_msg,
        )
    except Exception as e: 
        return jsonify(status = 500, error = e)

def editProduct(data, auth, mongo,handler):
    try: 
        if (not "dataDat" in data) or (len(data["dataDat"]) != 4) :
            return jsonify( status= 500, msg= "Trường data dat null hoặc thiếu" )
        if (not "dataNuoc" in data) or (len(data["dataNuoc"]) != 4) :
            return jsonify( status= 500, msg= "Trường data nuoc null hoặc thiếu" )
        if (not "dataGiong" in data) or (len(data["dataGiong"]) != 3) :
            return jsonify( status= 500, msg= "Trường data giong null hoặc thiếu" )
        if (not "dataInfo" in data) or (len(data["dataInfo"]) != 3) :
            return jsonify( status= 500, msg= "Trường data giong null hoặc thiếu" )
        product_collection = mongo.db.products
        getProduct = product_collection.find_one({"address_contract" : data["address_contract"]})
        dataSoil = data["dataDat"]
        dataWater = data["dataNuoc"]
        dataGenus = data["dataGiong"]
        dataProduct = data["dataInfo"]
        if setblc.setSoil(getProduct["soil_id"] ,dataSoil, getProduct["product_id"], handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        if setblc.setWater(getProduct["water_id"], dataWater, getProduct["product_id"], handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        if setblc.setGenus(getProduct["genus_id"], dataGenus, getProduct["product_id"], handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        if setblc.setProduct(getProduct["product_id"], dataProduct, mongo, handler) == False: 
            return jsonify(status = 500 , msg = "fail soil")
        return jsonify(  status =  200, msg =  "Ghi thông tin thành công" )
        
    except Exception as e: 
        return jsonify(status = 500, error = e)

def sendVerifyProduct(data, userid, mongo):
    try: 
        msg_collection = mongo.db.msg
        product_collection = mongo.db.products

        tx_hash = data["address_contract"]
        reqType = data["type"]
        
        checkExistType = msg_collection.find_one({"address_contract" : tx_hash, "type" : reqType})

        if checkExistType and checkExistType["status"] != "3" :
            return jsonify(status = 200, msg = "The request has been accepted")

        getProduct = product_collection.find_one({"address_contract" : tx_hash, "user_id" : ObjectId(userid)})
        now = datetime.datetime.now()
        if "result" not in data:
            data = {
                "user_id": ObjectId(userid),
                "user_id_lien_group": getProduct["parent_id"],
                "product_id" : getProduct["_id"],
                "type" : str(reqType),
                "address_contract" : tx_hash,
                "status" : 1, 
                "updateAt" : now
            }
        else: 
            data = {
                "user_id": ObjectId(userid),
                "user_id_lien_group": getProduct["parent_id"],
                "product_id" : getProduct["_id"],
                "type" : str(reqType),
                "address_contract" : tx_hash,
                "status" : 1, 
                "updateAt" : now,
                "result" : str(data["result"])
            }
        msg_collection.insert(data)
        return jsonify(status = 200)
    except Exception as e: 
        return jsonify(status = 500, error = e)

def setVerifyProduct(data, userid, mongo):
    try: 
        msg_collection = mongo.db.msg
        product_collection = mongo.db.products
        user_collection = mongo.db.users

        msgId = data["msg_id"]

        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        if getInfodUserById["role"] != "1":
            return jsonify(status = 500, msg = "you are not admin list group" )

        result = msg_collection.find_one({"_id" : ObjectId(msgId)})
        
        filter = { '_id': result["product_id"]}
        # Values to be updated.
        newvalues = { "$set": { "status" : True, }} 
        
        # Using update_one() method for single updation.
        product_collection.update_one(filter, newvalues)

        now = datetime.datetime.now()
        filter1 = { '_id': ObjectId(msgId) }
        # Values to be updated.
        newvalues1 = { "$set": { "status" : 2, "updateAt" : now}} 
        
        # Using update_one() method for single updation.
        msg_collection.update_one(filter1, newvalues1) 
        
        return jsonify(status = 200, msg = "Accepted")
    except Exception as e: 
        return jsonify(status = 500, error = e)

def getListMsg(userid, mongo):
    try: 
        user_collection = mongo.db.users
        msg_collection = mongo.db.msg

        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})
        if getInfodUserById["role"] != "1" :
            return jsonify(status = 500, msg = "You are not admin list group")

        items = []        
        getAllMsg = msg_collection.find({"user_id_lien_group" : ObjectId(userid)})

        for document in getAllMsg: 
            get_user = user_collection.find_one({"_id" : document["user_id"]})
            document["user_id"] = get_user["email"]
            temp = str(document["_id"])
            document["_id"] = temp
            temp = str(document["user_id_lien_group"])
            document["user_id_lien_group"] = temp
            temp = str(document["product_id"])
            document["product_id"] = temp
            items.append(document)
        print(items)   
        return jsonify(status = 200, items = items)
    except Exception as e: 
        return jsonify(status = 500, error = e) 

def rejectVerify(data, mongo):
    try: 
        msg_collection = mongo.db.msg

        msgId = data["msg_id"]

        now = datetime.datetime.now()
        filter1 = { '_id': ObjectId(msgId) }
        # Values to be updated.
        newvalues1 = { "$set": { "status" : 3, "updateAt" : now}} 
        
        # Using update_one() method for single updation.
        msg_collection.update_one(filter1, newvalues1)
        
        return jsonify(status = 200, msg = "Rejected")
        
    except Exception as e: 
        return jsonify(status = 500, error = e)

def getListAction(tx_hash, userId, mongo, handler):
    try: 
        user_colleciton = mongo.db.users
        product_collection = mongo.db.products
        
        getInfodUserById = user_colleciton.find_one({"_id" : ObjectId(userId)})
        getProduct = product_collection.find_one({"address_contract" : tx_hash})

        role = getInfodUserById["role"]

        if role != "2":
            return jsonify(status = 500, msg= "You are not admin group")
        
        if not getProduct : 
            return jsonify(status = 500, msg = "product is not empty")
        
        arr_action = getblc.getListAction(getProduct["product_id"], handler)
        items = []
        if len(arr_action) == 0: 
            return jsonify(status = 200, items = items)
        
        for document in arr_action: 
            print(document)
            action_info = getblc.getAction(document, handler)
            print(action_info)
            data = {
                "time" : action_info[2],
                "action_name" : action_info[1],
                "description" : action_info[3],
                "key" : action_info[0]
            }
            items.append(data)
        print(items)
        return jsonify(status = 200, items = items)
    except Exception as e: 
        return jsonify(status = 500, error = e) 

def setAction( data, userid, mongo, handler):
    try:
        # action_name = data["action_name"]
        # description = data["description"]
        print(data)
        address_contract = data["address_contract"]

        user_collection = mongo.db.users
        product_collection = mongo.db.products
        household_collection = mongo.db.households
        msgaction_collection = mongo.db.msg_actions
        
        getInfodUserById = user_collection.find_one({"_id" : ObjectId(userid)})

        role = getInfodUserById["role"]

        if (role != constant.Constants["Group"]):
            return jsonify(status = 500, msg=" Ban khong cos quyen tao action!")

        getProduct = product_collection.find_one({"address_contract" : address_contract})
        
        product_id = getProduct["product_id"]
        id = uuid.uuid1()
    
        getAllHousehold = household_collection.find({"parent_group_id": ObjectId(userid), "product_id": getProduct["_id"]})
        now = datetime.datetime.now()
        for document in getAllHousehold:
            data_insert={
                "user_id": ObjectId(userid),
                "user_id_household": document["user_id"],
                "status":0,
                "address_contract": address_contract,
                "key_action" : str(id),
                "data": "", 
                "updateAt" : now,
            }
            msgaction_collection.insert(data_insert)
        set_action = setblc.setAction(str(id), data, product_id, handler)
        if set_action == False: 
            return jsonify(status = 500, msg = "Fail")
        return jsonify(status=200, msg="Tao Action thanh cong")
    except Exception as e: 
        return jsonify(status = 500, error = e)

def getAction(tx_hash, action_id, userid, mongo, handler):
    try: 
        msgaciton_collection = mongo.db.msg_actions
        user_collection = mongo.db.users
        action_info = getblc.getAction(action_id, handler)
        getDataMsgAction = msgaciton_collection.find({"key_action" : action_id, "address_contract" : tx_hash})
        items = []
        for document in getDataMsgAction:
            getInfoHouseHold = user_collection.find_one({"_id" : document["user_id_household"]})
            email_user = getInfoHouseHold["email"]
            document["user_id_household"] = email_user
            temp = str(document["_id"])
            document["_id"] = temp
            temp = str(document["user_id"])
            document["user_id"] = temp
            items.append(document)
        data = {
            "time": action_info[2],
            "action_name" : action_info[1],
            "description" : action_info[3],
            "key" : action_id,
            "msg_action" : items
        }
        return jsonify(status = 200, data = data)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)    

def getMsgActionForFarmer(tx_hash, userid, mongo):
    try: 
        msgaction_collection = mongo.db.msg_actions
        getMsgAction = msgaction_collection.find({"user_id_household" : ObjectId(userid), "address_contract" : tx_hash})
        items = []
        now = datetime.datetime.now()
        print(now)
        for document in getMsgAction:
            temp = str(document["user_id_household"])
            document["user_id_household"] = temp
            temp = str(document["_id"])
            document["_id"] = temp
            temp = str(document["user_id"])
            document["user_id"] = temp
            items.append(document)
        
        return jsonify(status = 200, items = items)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def setStatusAction(data, mongo):
    try: 
        msgaction_collection = mongo.db.msg_actions
        msgActionId = data["msg_action_id"]
        status = data["status"]
        now = datetime.datetime.now()
        filter = { '_id': ObjectId(msgActionId) }
        
        # Values to be updated.
        newvalues = { "$set": { 'status': status, 'updateAt' : now }} 
        msgaction_collection.update_one(filter, newvalues) 

        
        return jsonify(status = 200, msg = "updated")
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)
    
def setHistory(data, userid, mongo, handler):
    try: 
        user_collection = mongo.db.users
        product_collection = mongo.db.products
        msgaction_collection = mongo.db.msg_actions
        history_collection = mongo.db.historys
        transaction_collection = mongo.db.transactions

        print(data)

        tx_hash = data["address_contract"]
        action_id = data["key_qrcode"]
        msg_action_id = data["msg_action_id"]

        now = datetime.datetime.now()

        getProduct = product_collection.find_one({"address_contract": tx_hash})        

        getMsgAction = msgaction_collection.find_one({"_id" : ObjectId(msg_action_id)})

        getFarmer = user_collection.find_one({"_id" : getMsgAction["user_id_household"]})

        id = uuid.uuid1()

        set_history = setblc.setHistory(id,action_id, getFarmer["email"], getMsgAction["updateAt"], handler)
        if set_history["msg"] == False: 
            return jsonify(status = 500, msg = "Fail")
        transaction_collection.insert({"contract_id" : tx_hash,"tx" : set_history["tx_hash_history"], "updateAt" : str(now)})
        filter = { '_id': ObjectId(msg_action_id) }
        
        # Values to be updated.
        newvalues = { "$set": { 'status': 2, 'updateAt' : now }} 
        msgaction_collection.update_one(filter, newvalues) 
        history_collection.insert({"history_id" : str(id), "product_id":getProduct["product_id"]})
        return jsonify(status = 200, msg = "complete" , tx = set_history["tx_hash_history"])
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def getHistory(tx_hash, userid, mongo, handler):
    try: 
        history_collection = mongo.db.historys
        product_collection = mongo.db.products

        getProduct = product_collection.find_one({"address_contract" : tx_hash})
        getIdHistory = history_collection.find({"product_id" : getProduct["product_id"]})

        items = []
        for document in getIdHistory: 
            historyInfo = getblc.getHistory(document["history_id"], handler)
            actionInfo = getblc.getAction(historyInfo[4], handler)
            data = {
                "time" : historyInfo[1],
                "action_name" : actionInfo[1],
                "key_qrcode" : actionInfo[0],
                "description" : historyInfo[2]
            }
            items.append(data)
        print(items)
        return jsonify(status = 200, data = items)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def getAllInfo(data, userid, mongo, handler):
    try: 
        tx_hash = data["address_contract"]

        history_collection = mongo.db.historys
        product_collection = mongo.db.products
        msg_collection = mongo.db.msg
        transaction_collection = mongo.db.transactions

        getProduct = product_collection.find_one({"address_contract" : tx_hash})
        
        data_info = getProduct["data_info"]

        resultProduct = getblc.getProduct(getProduct["product_id"], handler)

        resultGetSoild = getblc.getSoil(getProduct["soil_id"], handler)

        resultGetWater = getblc.getWater(getProduct["water_id"], handler)

        resultGetGenus = getblc.getGenus(getProduct["genus_id"], handler)

        respInfo = {
            "name": "Thông tin mùa vụ",
            "data": [
            {
                "name": "Tên",
                "data": data_info[0],
            },
            {
                "name": "Địa điểm",
                "data": data_info[1],
            },
            {
                "name": "Diện tích",
                "data": data_info[2],
            },
            ],
        }
        respSoil = {
            "name": "Thông tin về đất",
            "data": [
            {
                "name": "Loại đất",
                "data": resultGetSoild[1],
            },
            {
                "name": "Độ Ph",
                "data": resultGetSoild[2],
            },
            {
                "name": "Vị trí",
                "data": resultGetSoild[3],
            },
            {
                "name": "Miêu tả",
                "data": resultGetSoild[4],
            },
            ],
        }
        respWater = {
            "name": "Thông tin về nguồn nước",
            "data": [
            {
                "name": "Nguồn gốc",
                "data": resultGetWater[1],
            },
            {
                "name": "Độ Ph",
                "data": resultGetWater[2],
            },
            {
                "name": "Vị trí",
                "data": resultGetWater[3],
            },
            {
                "name": "Miêu tả",
                "data": resultGetWater[4],
            },
            ],
        }

        respGenus = {
            "name": "Thông tin về giống cây",
            "data": [
            {
                "name": "Tên giống",
                "data": resultGetGenus[1],
            },
            {
                "name": "Nguồn gốc",
                "data": resultGetGenus[2],
            },
            {
                "name": "Miêu tả",
                "data": resultGetGenus[3],
            },
            ],
        }

        getIdHistory = history_collection.find({"product_id" : getProduct["product_id"]})

        resultHistory = []
        for document in getIdHistory: 
            historyInfo = getblc.getHistory(document["history_id"], handler)
            actionInfo = getblc.getAction(historyInfo[4], handler)
            data = {
                "time" : historyInfo[1],
                "action_name" : actionInfo[1],
                "key_qrcode" : actionInfo[0],
                "description" : historyInfo[2]
            }
            resultHistory.append(data)
        getMsg = msg_collection.find_one({"address_contract" : tx_hash, "type" : "2", "status" : 1})
        result = ''
        if not getMsg: 
            getMsgRejected =  msg_collection.find_one({"address_contract" : tx_hash, "type" : "2", "status" : 3})
            if getMsgRejected: 
                status_msg = 3
            else: 
                status_msg = ''
        else: 
            status_msg = getMsg["status"]
            result = getMsg["result"]
        getMsgConfirm = msg_collection.find_one({"address_contract" : tx_hash, "type" : "2", "status" : 2})
        if getMsgConfirm: 
            status_msg = getMsgConfirm["status"]
            end = True
            result = resultProduct[5]
        else : 
            end = False
        print(result + "- " + resultProduct[5])

        transInfo = transaction_collection.find({"contract_id" : tx_hash})
        respTx = []
        for document in transInfo :
            temp = str(document["_id"]) 
            document["_id"] = temp
            respTx.append(document)
        
        print(respTx)

        return jsonify(status = 200,
        resp_info = respInfo,
        resp_dat = respSoil,
        resp_giong = respGenus,
        resp_nuoc = respWater,
        resp_history =  resultHistory,
        end_smart_contract = end,
        result = result,
        resp_tx= respTx,
        status_msg =  status_msg)
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)

def setResultProduct(data, userid, mongo, handler):
    try: 
        msgId = data["msg_id"]

        user_collection = mongo.db.users
        product_collection = mongo.db.products
        msg_collection = mongo.db.msg

        getUser = user_collection.find_one({"_id" : ObjectId(userid)})

        getMsg = msg_collection.find_one({"_id" : ObjectId(msgId)})

        getProduct = product_collection.find_one({"address_contract" : getMsg["address_contract"]})

        if not getUser or getUser["role"] != "1":
            return jsonify(status = 500, msg = "You are not admin")
        
        setResult = setblc.setResult(getProduct["product_id"], getMsg["result"], handler)

        if setResult == False: 
            return jsonify(status = 500, msg = "Fail")
        now = datetime.datetime.now()
        filter = { '_id': ObjectId(msgId) }
        
        # Values to be updated.
        newvalues = { "$set": { 'status': 2, 'updateAt' : now}} 
        msg_collection.update_one(filter, newvalues)

        
        return jsonify(status = 200, msg = "updated")
    except Exception as e: 
        print(e)
        return jsonify(status = 500, error = e)      