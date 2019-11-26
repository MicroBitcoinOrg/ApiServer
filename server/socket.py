from server.methods.transaction import Transaction
from server.methods.general import General
from server.methods.address import Address
from server import socket_stats
from server import utils
from server import sio

@socket_stats
def GetInfo():
	return General().info()

@socket_stats
def EstimateFee():
	return General().fee()

@socket_stats
def AddressUnspent(address: str, amount=0):
	return Address().unspent(address, amount)

@socket_stats
def AddressBalance(address: str):
	return Address().balance(address)

@socket_stats
def AddressHistory(address: str):
	return Address().history(address)

@socket_stats
def AddressMempool(address: str):
	return Address().mempool(address)

@socket_stats
def AddressMempoolRaw(address: str):
	return Address().mempool(address, True)

@socket_stats
def TransactionInfo(thash: str):
	return Transaction().info(thash)

@socket_stats
def Broadcast(raw: str):
	return Transaction().broadcast(raw)

@socket_stats
def CheckHistory(addresses: list):
	return Address().check(addresses)

@socket_stats
def TransactionBatch(hashes: list):
	result = []
	for thash in hashes:
		result.append(Transaction().info(thash))

	return utils.response(result)

sio.on_event('general.info', GetInfo)
sio.on_event('general.fee', EstimateFee)
sio.on_event('address.unspent', AddressUnspent)
sio.on_event('address.balance', AddressBalance)
sio.on_event('address.history', AddressHistory)
sio.on_event('address.mempool', AddressMempool)
sio.on_event('address.mempool.raw', AddressMempoolRaw)
sio.on_event('address.check', CheckHistory)
sio.on_event('transaction.info', TransactionInfo)
sio.on_event('transaction.broadcast', Broadcast)
sio.on_event('transaction.batch', TransactionBatch)
