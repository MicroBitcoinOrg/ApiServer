from server.methods.transaction import Transaction
from server import utils

class Block():
	@classmethod
	def height(cls, height: int):
		data = utils.make_request('getblockhash', [height])

		if data['error'] is None:
			txid = data['result']
			data.pop('result')
			data['result'] = utils.make_request('getblock', [txid])['result']
			data['result']['txcount'] = len(data['result']['tx'])
			data['result'].pop('nTx')

		return data

	@classmethod
	def hash(cls, bhash: str):
		data = utils.make_request('getblock', [bhash])

		if data['error'] is None:
			data['result']['txcount'] = len(data['result']['tx'])
			data['result'].pop('nTx')

		return data

	@classmethod
	def get(cls, height: int):
		return utils.make_request('getblockhash', [height])

	@classmethod
	def range(cls, height: int, offset: int):
		result = []
		for block in range(height - (offset - 1), height + 1):
			data = utils.make_request('getblockhash', [block])
			nethash = utils.make_request('getnetworkhashps', [120, block])

			if data['error'] is None and nethash['error'] is None:
				txid = data['result']
				data.pop('result')
				data['result'] = utils.make_request('getblock', [txid])['result']
				data['result']['txcount'] = len(data['result']['tx'])
				data['result']['nethash'] = int(nethash['result'])
				data['result'].pop('nTx')

				result.append(data['result'])

		return result[::-1]

	@classmethod
	def inputs(cls, bhash: str):
		data = cls.hash(bhash)
		return Transaction().addresses(data['result']['tx'])
