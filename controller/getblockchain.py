from os import error

def getGenus(idGenus, handler) :
    try: 
        result = handler.get_genus(idGenus)
        print(result)
        return result
    except Exception as e: 
        return e

def getWater(idWater, handler) :
    try: 
        result = handler.get_water(idWater)
        return result
    except Exception as e: 
        return e

def getSoil(idSoil, handler) :
    try: 
        result = handler.get_soil(idSoil)
        return result
    except Exception as e: 
        return e       

def getListAction(idProduct, handler):
    try: 
        result = handler.get_product(idProduct)
        return result[10]
    except Exception as e: 
        return e 

def getAction(idAction, handler): 
    try: 
        result = handler.get_action(idAction)
        return result
    except Exception as e: 
        return e 

def getHistory(idHistory, handler): 
    try: 
        result = handler.get_history(idHistory)
        return result
    except Exception as e: 
        return e 

def getProduct(idProduct, handler): 
    try: 
        result = handler.get_product(idProduct)
        return result
    except Exception as e: 
        return e 
