from server.methods.transaction import Transaction
from server.methods.general import General
from server.methods.address import Address
from server import subscription
from server import stats
from server import utils

@stats.socket
def GetInfo():
    return General().info()

@stats.socket
def EstimateFee():
    return General().fee()

@stats.socket
def AddressUnspent(address=None, amount=0):
    return Address().unspent(address, amount)

@stats.socket
def AddressBalance(address=None):
    return Address().balance(address)

@stats.socket
def AddressHistory(address=None):
    return Address().history(address)

@stats.socket
def AddressMempool(address=None):
    return Address().mempool(address)

@stats.socket
def AddressMempoolRaw(address=None):
    return Address().mempool(address, True)

@stats.socket
def TransactionInfo(thash=None):
    return Transaction().info(thash)

@stats.socket
def Broadcast(raw=None):
    return Transaction().broadcast(raw)

@stats.socket
def CheckHistory(addresses=[]):
    return Address().check(addresses)

@stats.socket
def TransactionBatch(hashes=[]):
    result = []
    for thash in hashes:
        result.append(Transaction().info(thash))

    return utils.response(result)

def init(sio):
    sio.on_event("connect", subscription.Connect)
    sio.on_event("subscribe.address", subscription.SubscribeAddress)
    sio.on_event("subscribe.blocks", subscription.SubscribeBlocks)
    sio.on_event("unsubscribe.address", subscription.UnubscribeAddress)
    sio.on_event("unsubscribe.blocks", subscription.UnsubscribeBlocks)
    sio.on_event("disconnect", subscription.Disconnect)

    sio.on_event("general.info", GetInfo)
    sio.on_event("general.fee", EstimateFee)
    sio.on_event("address.unspent", AddressUnspent)
    sio.on_event("address.balance", AddressBalance)
    sio.on_event("address.history", AddressHistory)
    sio.on_event("address.mempool", AddressMempool)
    sio.on_event("address.mempool.raw", AddressMempoolRaw)
    sio.on_event("address.check", CheckHistory)
    sio.on_event("transaction.info", TransactionInfo)
    sio.on_event("transaction.broadcast", Broadcast)
    sio.on_event("transaction.batch", TransactionBatch)
