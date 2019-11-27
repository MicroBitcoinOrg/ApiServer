from server import socket_counter
from server import rest_counter
from datetime import timedelta
from server import subscribers
from server import connections
from server import start_time
from server import rooms
import server
import time

def socket(func):
	def wrapper(*args, **kwargs):
		global socket_counter
		socket_counter += 1
		return func(*args, **kwargs)

	return wrapper

def rest(func):
	def wrapper(*args, **kwargs):
		global rest_counter
		rest_counter += 1
		return func(*args, **kwargs)

	return wrapper

def info():
	global socket_counter
	global rest_counter
	global subscribers
	global connections
	global start_time
	global rooms

	uptime = timedelta(seconds=time.monotonic() - start_time)
	return {
		'uptime': str(uptime),
		'subscriptions': {
			'connections': server.connections,
			'subscribers': len(subscribers),
			'rooms': len(rooms)
		},
		'requests': {
			'socket': socket_counter,
			'rest': rest_counter
		}
	}
