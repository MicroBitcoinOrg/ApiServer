from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from methods.general import General
from methods.address import Address
from methods.block import Block
from flask_restful import Api
import core.config as config
import core.socket as socket
from flask_cors import CORS
import core.utils as utils
import core.rest as rest
import flask_socketio
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
sio = SocketIO(app, cors_allowed_origins='*')
api = Api(app)
CORS(app)

thread = None
subscribers = {}
rooms = {}

rest.init(api)
socket.init(sio)

def blocks_thread():
	bestblockhash = ''
	while True:
		data = General().info()
		if data['result']['bestblockhash'] != bestblockhash:
			bestblockhash = data['result']['bestblockhash']
			sio.emit('block.update', utils.response({
					'height': data['result']['blocks'],
					'hash': bestblockhash
				}), room='blocks')

			updates = Block().inputs(bestblockhash)
			for address in updates:
				if address in rooms:
					sio.emit('address.update', utils.response({
						'address': address,
						'balance': Address().balance(address)['result'],
						'tx': updates[address],
						'height': data['result']['blocks'],
						'hash': bestblockhash
					}), room=address)

		time.sleep(1)

@sio.on('connect')
def user_connect():
	global thread
	if thread is None:
		thread = sio.start_background_task(target=blocks_thread)

@sio.on('disconnect')
def user_disconnect():
	if request.sid in subscribers:
		for room in subscribers[request.sid]:
			if request.sid in rooms[room]:
				rooms[room].remove(request.sid)
				flask_socketio.leave_room(room, request.sid)
				if len(rooms[room]) == 0:
					rooms.pop(room)

		subscribers.pop(request.sid)

@sio.on('subscribe.blocks')
def user_subscribe_blocks():
	if request.sid not in subscribers:
		subscribers[request.sid] = []

	if 'blocks' not in rooms:
		rooms['blocks'] = [request.sid]
	else:
		rooms['blocks'].append(request.sid)

	subscribers[request.sid].append('blocks')
	flask_socketio.join_room('blocks', request.sid)

	return True

@sio.on('subscribe.address')
def user_subscribe_address(address):
	if request.sid not in subscribers:
		subscribers[request.sid] = []

	if address not in rooms:
		rooms[address] = [request.sid]
	else:
		rooms[address].append(request.sid)

	subscribers[request.sid].append(address)
	flask_socketio.join_room(address, request.sid)

	return True

@app.errorhandler(404)
def page_404(error):
	return jsonify(utils.dead_response('Method not found'))

if __name__ == '__main__':
	app.run(debug=config.debug, host=config.host, port=config.port)
