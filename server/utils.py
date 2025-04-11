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
    rate = 0.18 if height > 2650000 else 0.3
    r = 1 + (math.log(1 - rate) / (525960 * 2))
    return int((5500 * 10000) * math.pow(r, height))


def satoshis(value, decimals=4):
    return int(float(value) * math.pow(10, decimals))


def amount(value, decimals=4):
    return round(float(value) / math.pow(10, decimals), decimals)


def is_int(string):
    try:
        int(string)
        return True
    except Exception:
        return False
