from flask import Flask, jsonify
from flask_restful import Api
import backend.methods as methods
import backend.config as config
import backend.utils as utils
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(methods.GetInfo, '/info')
api.add_resource(methods.BlockByHeight, '/height/<int:height>')
api.add_resource(methods.BlockByHash, '/block/<string:bhash>')
api.add_resource(methods.BlockHeader, '/header/<string:bhash>')
api.add_resource(methods.BlocksByRange, '/range/<int:height>')
api.add_resource(methods.AddressBalance, '/balance/<string:address>')
api.add_resource(methods.AddressMempool, '/mempool/<string:address>')
api.add_resource(methods.AddressUnspent, '/unspent/<string:address>')
api.add_resource(methods.AddressTransactions, '/history/<string:address>')
api.add_resource(methods.TransactionInfo, '/transaction/<string:thash>')
api.add_resource(methods.DecodeRawTx, '/decode/<string:raw>')
api.add_resource(methods.MempoolInfo, '/mempool')
api.add_resource(methods.Supply, '/supply')
api.add_resource(methods.EstimateFee, '/fee')
api.add_resource(methods.Broadcast, '/broadcast')

@app.errorhandler(404)
def own_404_page(error):
	return jsonify(utils.dead_response(32601, 'Method not found'))

if __name__ == '__main__':
	app.run(debug=config.debug, host=config.host, port=config.port)
