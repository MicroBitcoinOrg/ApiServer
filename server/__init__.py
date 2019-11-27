from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
from flask_caching import Cache
from datetime import timedelta
from flask_restful import Api
from flask_cors import CORS
from server import utils
import flask_socketio
import config
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
cache = Cache(config={'CACHE_TYPE': 'simple'})
sio = SocketIO(app, cors_allowed_origins='*')
cache.init_app(app)
api = Api(app)
CORS(app)

start_time = time.monotonic()
socket_counter = 0
rest_counter = 0

thread = None
connections = 0
subscribers = {}
mempool = []
rooms = {}

def socket_stats(func):
	def wrapper(*args, **kwargs):
		global socket_counter
		socket_counter += 1
		return func(*args, **kwargs)

	return wrapper

def rest_stats(func):
	def wrapper(*args, **kwargs):
		global rest_counter
		rest_counter += 1
		return func(*args, **kwargs)

	return wrapper

from server.methods.transaction import Transaction
from server.methods.general import General
from server.methods.block import Block
from server import socket
from server import rest

def blocks_thread():
	global subscribers
	global mempool
	global rooms

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
				mempool = list(set(mempool) - set(updates[address]))
				if address in rooms:
					sio.emit('address.update', utils.response({
						'address': address,
						'tx': updates[address],
						'height': data['result']['blocks'],
						'hash': bestblockhash
					}), room=address)

		data = General().mempool()
		updates = Transaction().addresses(data['result']['tx'])
		temp_mempool = []
		for address in updates:
			updates[address] = list(set(updates[address]) - set(mempool))
			temp_mempool += updates[address]
			if address in rooms:
				if len(updates[address]) > 0:
					sio.emit('address.update', utils.response({
						'address': address,
						'tx': updates[address],
						'height': None,
						'hash': None
					}), room=address)

		mempool = list(set(mempool + temp_mempool))

@sio.on('connect')
def user_connect():
	global connections
	global thread
	connections += 1

	if thread is None:
		thread = sio.start_background_task(target=blocks_thread)

@sio.on('disconnect')
def user_disconnect():
	global connections
	connections -= 1

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

@app.route('/stats')
def app_stats():
	uptime = timedelta(seconds=time.monotonic() - start_time)
	return jsonify({
			'uptime': str(uptime),
			'subscriptions': {
				'connections': connections,
				'subscribers': len(subscribers),
				'rooms': len(rooms)
			},
			'requests': {
				'socket': socket_counter,
				'rest': rest_counter
			}
		})

@app.route('/')
def frontend():
	return render_template('index.html')

@app.errorhandler(404)
def page_404(error):
	return jsonify(utils.dead_response('Method not found'))
