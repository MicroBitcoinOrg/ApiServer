from flask_restful import Resource, reqparse
from flask_restful import inputs
import backend.utils as utils

class GetInfo(Resource):
	def get(self):
		data = utils.make_request('getblockchaininfo')

		if data['error'] is None:
			data['result']['reward'] = utils.reward(data['result']['blocks'])
			data['result'].pop('verificationprogress')
			data['result'].pop('initialblockdownload')
			data['result'].pop('pruned')
			data['result'].pop('softforks')
			data['result'].pop('bip9_softforks')
			data['result'].pop('warnings')
			data['result'].pop('size_on_disk')

		return data

class BlockByHeight(Resource):
	def get(self, height):
		parser = reqparse.RequestParser()
		parser.add_argument('offset', type=int, default=0)
		parser.add_argument('hash', type=inputs.boolean, default=0)
		args = parser.parse_args()

		data = utils.make_request('getblockhash', [height])

		if data['error'] is None and not args['hash']:
			txid = data['result']
			data.pop('result')
			data['result'] = utils.make_request('getblock', [txid])['result']
			data['result']['txcount'] = len(data['result']['tx'])
			data['result']['tx'] = data['result']['tx'][args['offset']:args['offset'] + 10]
			data['result'].pop('nTx')

		return data

class BlocksByRange(Resource):
	def get(self, height):
		parser = reqparse.RequestParser()
		parser.add_argument('offset', type=int, default=30)
		args = parser.parse_args()

		result = []
		if args['offset'] > 100:
			args['offset'] = 100

		for block in range(height - (args['offset'] - 1), height + 1):
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

		return utils.response(result[::-1])

class BlockByHash(Resource):
	def get(self, bhash):
		parser = reqparse.RequestParser()
		parser.add_argument('offset', type=int, default=0)
		args = parser.parse_args()

		data = utils.make_request('getblock', [bhash])

		if data['error'] is None:
			data['result']['txcount'] = len(data['result']['tx'])
			data['result']['tx'] = data['result']['tx'][args['offset']:args['offset'] + 10]
			data['result'].pop('nTx')

		return data

class BlockHeader(Resource):
	def get(self, bhash):
		data = utils.make_request('getblockheader', [bhash])
		if data['error'] is None:
			data['result']['txcount'] = data['result']['nTx']
			data['result'].pop('nTx')

		return data

class TransactionInfo(Resource):
	def get(self, thash):
		data = utils.make_request('getrawtransaction', [thash, True])

		if data['error'] is None:
			if 'blockhash' in data['result']:
				block = utils.make_request('getblock', [data['result']['blockhash']])['result']
				data['result']['height'] = block['height']
			else:
				data['result']['height'] = -1

			if data['result']['height'] != 0:
				for index, vin in enumerate(data['result']['vin']):
					if 'txid' in vin:
						vin_data = utils.make_request('getrawtransaction', [vin['txid'], True])
						if vin_data['error'] is None:
							data['result']['vin'][index]['scriptPubKey'] = vin_data['result']['vout'][vin['vout']]['scriptPubKey']
							data['result']['vin'][index]['value'] = utils.satoshis(vin_data['result']['vout'][vin['vout']]['value'])

			amount = 0
			for index, vout in enumerate(data['result']['vout']):
				data['result']['vout'][index]['value'] = utils.satoshis(vout['value'])
				amount += vout['value']

			data['result']['amount'] = amount

		return data

class AddressBalance(Resource):
	def get(self, address):
		data = utils.make_request('getaddressbalance', [address])

		return data

class AddressTransactions(Resource):
	def get(self, address):
		parser = reqparse.RequestParser()
		parser.add_argument('offset', type=int, default=0)
		args = parser.parse_args()

		data = utils.make_request('getaddresstxids', [address])

		if data['error'] is None:
			data['result'] = data['result'][::-1]
			total = len(data['result'])
			transactions = data['result'][args['offset']:args['offset'] + 10]
			data.pop('result')
			data['result'] = {}
			data['result']['tx'] = transactions
			data['result']['txcount'] = total

		return data

class AddressMempool(Resource):
	def get(self, address):
		data = utils.make_request('getaddressmempool', [address])

		if data['error'] is None:
			total = len(data['result'])
			transactions = data['result']

			for index, tx in enumerate(transactions):
				transactions[index].pop('address')

			data.pop('result')
			data['result'] = {}
			data['result']['tx'] = transactions
			data['result']['txcount'] = total

		return data

class AddressUnspent(Resource):
	def get(self, address):
		parser = reqparse.RequestParser()
		parser.add_argument('amount', type=int, default=0)
		args = parser.parse_args()

		data = utils.make_request('getaddressutxos', [address, utils.amount(args['amount'])])

		if data['error'] is None:
			utxos = []
			for index, utxo in enumerate(data['result']):
				utxos.append({
						'txid': utxo['txid'],
						'index': utxo['outputIndex'],
						'script': utxo['script'],
						'value': utxo['satoshis'],
						'height': utxo['height']
					})

			data['result'] = utxos

		return data

class MempoolInfo(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('offset', type=int, default=0)
		args = parser.parse_args()

		data = utils.make_request('getmempoolinfo')

		if data['error'] is None:
			if data['result']['size'] > 0:
				mempool = utils.make_request('getrawmempool')['result']
				data['result']['tx'] = mempool[args['offset']:args['offset'] + 10]
			else:
				data['result']['tx'] = []

		return data

class DecodeRawTx(Resource):
	def get(self, raw):
		data = utils.make_request('decoderawtransaction', [raw])
		return data

class EstimateFee(Resource):
	def get(self):
		data = utils.make_request('estimatesmartfee', [6])

		if data['error'] is None:
			data['result']['feerate'] = utils.satoshis(data['result']['feerate'])

		return data

class Broadcast(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('raw', type=str, default="")
		args = parser.parse_args()

		return utils.make_request('sendrawtransaction', [args['raw']])

class Supply(Resource):
	def get(self):
		supply = 443863973624633
		data = utils.make_request('getblockchaininfo')
		height = data['result']['blocks']
		for height in range(0, height + 1):
			supply += utils.reward(height)

		return utils.response({
				'supply': supply,
				'height': height
			})
