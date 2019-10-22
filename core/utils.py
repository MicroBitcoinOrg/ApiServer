import core.config as config
import requests
import math
import json

def dead_response(message='Invalid Request', rid=config.rid):
	return {'error': {'code': 404, 'message': message}, 'id': rid}

def response(result, error=None, rid=config.rid):
	return {'error': error, 'id': rid, 'result': result}

def make_request(method, params=[]):
	headers = {'content-type': 'text/plain;'}
	data = json.dumps({'id': config.rid, 'method': method, 'params': params})
	
	try:
		return requests.post(config.endpoint, headers=headers, data=data).json()
	except Exception:
		return dead_response()

def reward(height):
	r = 1 + (math.log(1 - 0.3) / (525960 * 2))
	return int((5500 * 10000) * math.pow(r, height))

def satoshis(value):
	return int(value * math.pow(10, 4))

def amount(value):
	return round(value / math.pow(10, 4), 4)
