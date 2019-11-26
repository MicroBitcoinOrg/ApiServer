from server import utils
from server import cache
import config

class General():
	@classmethod
	def info(cls):
		data = utils.make_request('getblockchaininfo')

		if data['error'] is None:
			data['result']['reward'] = utils.reward(data['result']['blocks'])
			data['result']['debug'] = config.debug
			data['result'].pop('verificationprogress')
			data['result'].pop('initialblockdownload')
			data['result'].pop('pruned')
			data['result'].pop('softforks')
			data['result'].pop('bip9_softforks')
			data['result'].pop('warnings')
			data['result'].pop('size_on_disk')

		return data

	@classmethod
	@cache.memoize(timeout=config.cache)
	def supply(cls):
		supply = 0
		snapshot = 443863973624633
		data = utils.make_request('getblockchaininfo')
		height = data['result']['blocks']
		for height in range(0, height + 1):
			supply += utils.reward(height)

		return {
			'supply': snapshot + supply,
			'mining': supply,
			'height': height
		}

	@classmethod
	def fee(cls):
		data = utils.make_request('estimatesmartfee', [6])

		if data['error'] is None:
			data['result']['feerate'] = utils.satoshis(data['result']['feerate'])

		return data

	@classmethod
	def mempool(cls):
		data = utils.make_request('getmempoolinfo')

		if data['error'] is None:
			if data['result']['size'] > 0:
				mempool = utils.make_request('getrawmempool')['result']
				data['result']['tx'] = mempool
			else:
				data['result']['tx'] = []

		return data
