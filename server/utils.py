import requests
import config
import math
import json

def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid):
    return {"error": error, "id": rid, "result": result}

def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()

def reward(height):
    halvings = height // 2102400

    if halvings >= 64:
        return 0

    return int(satoshis(50.00000000) // (2 ** halvings))

def supply(height):
    # ---------Updated for WCN----------------
    getward_c1 = 3500000
    getward_c2 = 2499999       
    getward_c3 = 999980
    halvings_count = 0
    
    if height > 100000 and height <500000:
       calheight = height -  100001
       getward_c4 = calheight * 10
       sub_total_supply = getward_c1 + getward_c2 + getward_c3 + getward_c4 
       supply1 = sub_total_supply
    elif height > 500000 and height<=2102400:
        calheight = height - 500001
        getward_c5 = calheight * 5
        getward_c4 = 3999990 
        sub_total_supply = getward_c1 + getward_c2 + getward_c3 + getward_c4  + getward_c5
    #print('Info message:'+ str(calheight) +" reward:"+ str(getward_c3) +"tt:"+ str(sub_total_supply))
    else:
        getward_c4 = 3999990
        getward_c5 = 8011990

        reward = satoshis(5.00000000)
        halvings = 2102400
        supply = reward
        halvings_count = 0

        while height > halvings:
            total = halvings * reward
            reward = reward / 2
            height = height - halvings
            halvings_count += 1
            supply += total

        #supply = supply + height * reward
        supplybfhalving = getward_c1 + getward_c2 + getward_c3 + getward_c4 + getward_c5
        sub_total_supply = supplybfhalving+ (height * reward)
    # ---------End Updated----------------
    """reward = satoshis(50.00000000)
    halvings = 2102400
    halvings_count = 0
    supply = reward

    while height > halvings:
        total = halvings * reward
        reward = reward / 2
        height = height - halvings
        halvings_count += 1

        supply += total

    supply = supply + height * reward"""
    #logger.info(sub_total_supply)
    return {
        "halvings": int(halvings_count),
        #"supply": int(supply)
        "supply": int(str(sub_total_supply) + "00000000")
    }

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def amount(value):
    return round(value / math.pow(10, 8), 8)

def getprice():
    ticker = "WCN"
    coin_name = "Widecoin"
    price = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids="+coin_name+"&vs_currencies=usd,btc").json()
    price2 = requests.get(f"https://api.coinpaprika.com/v1/ticker/"+ticker+"-"+coin_name).json()
    if len(price)>0:
        btc = str(format(price[config.coin['coin_name']]["btc"], '.8f'))
        usd = str(price[config.coin['coin_name']]["usd"])
        msg = "Active"
    elif len(price2)>0:
        btc = float(price2["price_btc"])
        usd = float(price2["price_usd"])
        msg = "Active"           
    else:
         msg = "Error market cap connection"
    return {
        "price_btc": ('%.8f' % btc),
        "price_usd": ('%.8f' % usd),
        "status": msg
    }

