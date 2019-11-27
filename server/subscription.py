from server.methods.transaction import Transaction
from server.methods.general import General
from server.methods.block import Block
from flask import request
from server import stats
from server import utils
from server import sio
import server as state
import flask_socketio

def init():
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
				mempool = list(set(state.mempool) - set(updates[address]))
				if address in state.rooms:
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
			if address in state.rooms:
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
	state.connections += 1
	if state.thread is None:
		state.thread = sio.start_background_task(target=init)

@stats.socket
@sio.on('disconnect')
def user_disconnect():
	state.connections -= 1
	if request.sid in state.subscribers:
		for room in state.subscribers[request.sid]:
			if request.sid in state.rooms[room]:
				state.rooms[room].remove(request.sid)
				flask_socketio.leave_room(room, request.sid)
				if len(state.rooms[room]) == 0:
					state.rooms.pop(room)

		state.subscribers.pop(request.sid)

@stats.socket
@sio.on('subscribe.blocks')
def user_subscribe_blocks():
	if request.sid not in state.subscribers:
		state.subscribers[request.sid] = []

	if 'blocks' not in state.rooms:
		state.rooms['blocks'] = [request.sid]
	else:
		state.rooms['blocks'].append(request.sid)

	state.subscribers[request.sid].append('blocks')
	flask_socketio.join_room('blocks', request.sid)

	return True

@stats.socket
@sio.on('subscribe.address')
def user_subscribe_address(address):
	if request.sid not in state.subscribers:
		state.subscribers[request.sid] = []

	if address not in state.rooms:
		state.rooms[address] = [request.sid]
	else:
		state.rooms[address].append(request.sid)

	state.subscribers[request.sid].append(address)
	flask_socketio.join_room(address, request.sid)

	return True
