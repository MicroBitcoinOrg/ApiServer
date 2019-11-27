from server.methods.transaction import Transaction
from server.methods.general import General
from server.methods.block import Block
from server import subscribers
from server import mempool
from flask import request
from server import thread
from server import stats
from server import utils
from server import rooms
from server import sio
import server as state
import flask_socketio

def init():
	global subscribers
	global mempool
	global rooms

	bestblockhash = None

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

@stats.socket
@sio.on('connect')
def user_connect():
	global thread

	state.connections += 1
	if thread is None:
		thread = sio.start_background_task(target=init)

@stats.socket
@sio.on('disconnect')
def user_disconnect():
	global connections
	global subscribers
	global rooms

	state.connections -= 1
	if request.sid in subscribers:
		for room in subscribers[request.sid]:
			if request.sid in rooms[room]:
				rooms[room].remove(request.sid)
				flask_socketio.leave_room(room, request.sid)
				if len(rooms[room]) == 0:
					rooms.pop(room)

		subscribers.pop(request.sid)

@stats.socket
@sio.on('subscribe.blocks')
def user_subscribe_blocks():
	global subscribers
	global rooms

	if request.sid not in subscribers:
		subscribers[request.sid] = []

	if 'blocks' not in rooms:
		rooms['blocks'] = [request.sid]
	else:
		rooms['blocks'].append(request.sid)

	subscribers[request.sid].append('blocks')
	flask_socketio.join_room('blocks', request.sid)

	return True

@stats.socket
@sio.on('subscribe.address')
def user_subscribe_address(address):
	global subscribers
	global rooms

	if request.sid not in subscribers:
		subscribers[request.sid] = []

	if address not in rooms:
		rooms[address] = [request.sid]
	else:
		rooms[address].append(request.sid)

	subscribers[request.sid].append(address)
	flask_socketio.join_room(address, request.sid)

	return True
