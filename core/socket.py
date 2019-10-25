from methods.transaction import Transaction
from methods.general import General
from methods.address import Address

def init(sio):
	sio.on_event('general.info', GetInfo)
	sio.on_event('address.unspent', AddressUnspent)
	sio.on_event('address.balance', AddressBalance)
	sio.on_event('address.history', AddressHistory)
	sio.on_event('address.mempool', AddressMempool)
	sio.on_event('address.mempool.raw', AddressMempoolRaw)
	sio.on_event('address.check', CheckHistory)
	sio.on_event('transaction.info', TransactionInfo)
	sio.on_event('transaction.broadcast', Broadcast)


def GetInfo():
	return General().info()

def AddressUnspent(address: str, amount=0):
	return Address().unspent(address, amount)

def AddressBalance(address: str):
	return Address().balance(address)

def AddressHistory(address: str):
	return Address().history(address)

def AddressMempool(address: str):
	return Address().mempool(address)

def AddressMempoolRaw(address: str):
	return Address().mempool(address, True)

def TransactionInfo(thash: str):
	return Transaction().info(thash)

def Broadcast(raw: str):
	return Transaction().broadcast(raw)

def CheckHistory(addresses: list):
	return Address().check(addresses)
