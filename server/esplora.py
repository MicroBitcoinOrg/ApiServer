from flask import Response, Blueprint, jsonify, request
from server.methods.transaction import Transaction
from server.methods.address import Address
from server.methods.general import General
from server.methods.esplora import Esplora
from server.methods.block import Block
from server import stats
import config

blueprint = Blueprint("esplora", __name__)

@stats.rest
@blueprint.route("/block/<string:bhash>", methods=["GET"])
def block_hash(bhash):
    data = Block().hash(bhash)

    if data["error"] is None:
        result = data["result"]
        return Esplora().block(result)

    else:
        return Response("Block not found", mimetype="text/plain", status=404)

@stats.rest
@blueprint.route("/blocks", defaults={"height": None}, methods=["GET"])
@blueprint.route("/blocks/<int:height>", methods=["GET"])
def blocks_range(height):
    data = General.info()
    blocks = []

    if not height:
        height = data["result"]["blocks"]

    data = Block().range(height, config.block_page)

    for block in data:
        blocks.append(Esplora().block(block))

    return jsonify(blocks)

@stats.rest
@blueprint.route("/address/<string:address>", methods=["GET"])
def address_info(address):
    data = Address.history(address)

    if data["error"] is None:
        result = data["result"]
        mempool = Address.mempool(address)["result"]
        balance = Address.balance(address)["result"]

        # ToDo: Fix outputs count here

        return {
            "address": address,
            "chain_stats": {
                "funded_txo_count": 0,
                "funded_txo_sum": balance["received"],
                "spent_txo_count": 0,
                "spent_txo_sum": balance["received"] - balance["balance"],
                "tx_count": result["txcount"]
            },
            "mempool_stats": {
                "funded_txo_count": 0,
                "funded_txo_sum": 0,
                "spent_txo_count": 0,
                "spent_txo_sum": 0,
                "tx_count": mempool["txcount"]
            }
        }

    else:
        return Response("Invalid Bitcoin address", mimetype="text/plain", status=400)

@stats.rest
@blueprint.route("/block/<string:bhash>/status", methods=["GET"])
def block_status(bhash):
    data = Block().hash(bhash)
    next_best = None
    height = None
    best = False

    if data["error"] is None:
        result = data["result"]
        next_best = result["nextblockhash"] if "nextblockhash" in result else None
        height = result["height"]
        best = True

    return {
        "in_best_chain": best,
        "height": height,
        "next_best": next_best
    }

@stats.rest
@blueprint.route("/block/<string:bhash>/txs/<int:start>", methods=["GET"])
def block_transactions(bhash, start=0):
    data = Block().hash(bhash)
    transactions = []

    if start % config.tx_page != 0:
        return Response(f"start index must be a multipication of {config.tx_page}", mimetype="text/plain", status=400)

    if data["error"] is None:
        result = data["result"]

        for thash in result["tx"][start:start + config.tx_page]:
            transaction = Transaction.info(thash)["result"]
            transactions.append(Esplora().transaction(transaction))

        return jsonify(transactions)

    else:
        return Response("Block not found", mimetype="text/plain", status=404)

@stats.rest
@blueprint.route("/tx/<string:thash>", methods=["GET"])
def transaction_info(thash):
    data = Transaction.info(thash)

    if data["error"] is None:
        result = data["result"]
        return Esplora().transaction(result)

    else:
        return Response("Transaction not found", mimetype="text/plain", status=404)

@stats.rest
@blueprint.route("/tx/<string:thash>/outspends", methods=["GET"])
def transaction_spent(thash):
    data = Transaction.spent(thash)
    outputs = []

    if data["error"] is None:
        result = data["result"]
        for output in result:
            item = {"spent": output["spent"]}

            if output["spent"]:
                block = Block().height(output["height"])["result"]

                item["txid"] = output["txid"]
                item["vin"] = output["vin"]
                item["status"] = {
                    "confirmed": True,
                    "block_height": block["height"],
                    "block_hash": block["hash"],
                    "block_time": block["time"]
                }

            outputs.append(item)

        return jsonify(outputs)

    else:
        return Response("Transaction not found", mimetype="text/plain", status=404)

@stats.rest
@blueprint.route("/address/<string:address>/txs", defaults={"thash": None}, methods=["GET"])
@blueprint.route("/address/<string:address>/txs/chain/<string:thash>", methods=["GET"])
def address_transactions(address, thash):
    data = Address.history(address)
    transactions = []
    start = 0

    if data["error"] is None:
        result = data["result"]

        if thash in result["tx"]:
            start = result["tx"].index(thash) + 1

        for thash in result["tx"][start:start + config.tx_page]:
            transaction = Transaction.info(thash)["result"]
            transactions.append(Esplora().transaction(transaction))

        return jsonify(transactions)

    else:
        return Response("Invalid Bitcoin address", mimetype="text/plain", status=400)

@stats.rest
@blueprint.route("/block-height/<int:height>", methods=["GET"])
def plain_block_hash(height):
    data = Block().height(height)

    if data["error"] is None:
        return Response(data["result"]["hash"], mimetype="text/plain")

    else:
        return Response("Block not found", mimetype="text/plain", status=404)

@stats.rest
@blueprint.route("/blocks/tip/height", methods=["GET"])
def plain_tip_height():
    data = General.info()
    return Response(str(data["result"]["blocks"]), mimetype="text/plain")

@stats.rest
@blueprint.route("/mempool/recent", methods=["GET"])
def mempool_recent():
    data = General.mempool()
    result = []

    for txid in data["result"]["tx"]:
        transaction = Transaction.info(txid)["result"]
        item = Esplora().transaction(transaction)

        result.append({
            "txid": item["txid"],
            "fee": item["fee"],
            "vsize": item["weight"],
            "value": item["value"]
        })

    return jsonify(result)

@stats.rest
@blueprint.route("/tx", methods=["POST"])
def broadcast_tx():
    raw = request.data.decode("utf-8")
    data = Transaction.broadcast(raw)

    if data["error"] is None:
        return Response(data["result"], mimetype="text/plain")

    return Response(data["error"]["message"], mimetype="text/plain", status=400)

def init(app):
    app.register_blueprint(blueprint, url_prefix="/esplora")
