# Getting started
--------------

We have RESTful API which help you fetch info about MicroBitcoin blockchain and interact with it. This api is fetching data directrly from the full node with addres and transaction indexes enabled. Our [explorer](https://microbitcoinorg.github.io/explorer) and [web wallet](https://microbitcoinorg.github.io/wallet) is using this api.

# How to use it?
--------------

First of all you have to create `config.py` file in root of project directory with following content:

```
rid = 'api-server'
secret = 'Lorem ipsum dolor sit amet.'
endpoint = 'http://rpcuser:rpcpassword@127.0.0.1:6501/'
host = '0.0.0.0'
port = 1234
debug = True
```

All request should be send to this endpoint: `https://api.mbc.wiki`

Responce have following fields:

`result`: list or object which contains requested data
`error`: this field contains error message in case something went wrong
`id`: api server identifier which is set in `config.py` file

P.s. keep in mind, that all amounts in this API should be in **Satoshis**.

# Methods
--------------

## /info

This method return current info about MicroBitcoin blockchain.

Params: none

Request: https://api.mbc.wiki/info

Responce:
```
{
    "result": {
        "chain": "main",
        "blocks": 3568,
        "headers": 3568,
        "bestblockhash": "a7390c667198e96e88e55965d9af81c27ccc7b858cc3de07b623d6a89da7508d",
        "difficulty": 0.02024649845405542,
        "mediantime": 1570818535,
        "chainwork": "000000000000000000000000000000000000000000000000000000275ae68172",
        "reward": 54734486
    },
    "error": null,
    "id": "api-server"
}
```

## /height/<int:height>

This method return block info by given height.

Params:
`offset`: offset of transactions list (default: 0)
`hash`: return only hash of the block (default: false)

Request: https://api.mbc.wiki/height/0

Responce:
```
{
    "result": {
        "hash": "14c03ecf20edc9887fb98bf34b53809f063fc491e73f588961f764fac88ecbae",
        "minedhash": "001cb6047ddf13074c4bce354ed3cf0cdd96a4287aa562b032eb81d03e183da8",
        "confirmations": 3580,
        "size": 403750,
        "strippedsize": 403750,
        "weight": 1615000,
        "height": 0,
        "version": 1,
        "versionHex": "00000001",
        "merkleroot": "3426ccad3017e14a4ab6efddaa44cb31beca67a86c82f63de18705f1b6de88df",
        "tx": [
            "3426ccad3017e14a4ab6efddaa44cb31beca67a86c82f63de18705f1b6de88df"
        ],
        "time": 1570625829,
        "mediantime": 1570625829,
        "nonce": 709,
        "bits": "1f3fffff",
        "difficulty": 2.384149979653205e-07,
        "chainwork": "0000000000000000000000000000000000000000000000000000000000000400",
        "nextblockhash": "3fbdde4f2ccd683e4bae7d8867d1d647b21e5a90f3ae557c57e3f2b625d387d4",
        "txcount": 1
    },
    "error": null,
    "id": "api-server"
}
```

Request: https://api.mbc.wiki/height/0

Responce:
```
{
    "result": "14c03ecf20edc9887fb98bf34b53809f063fc491e73f588961f764fac88ecbae",
    "error": null,
    "id": "api-server"
}
```

## /block/<string:hash>

This method return block info by given hash.

Params:
`offset`: offset of transactions list (default: 0)

Request: https://api.mbc.wiki/block/14c03ecf20edc9887fb98bf34b53809f063fc491e73f588961f764fac88ecbae

Responce:
```
{
    "result": {
        "hash": "14c03ecf20edc9887fb98bf34b53809f063fc491e73f588961f764fac88ecbae",
        "minedhash": "001cb6047ddf13074c4bce354ed3cf0cdd96a4287aa562b032eb81d03e183da8",
        "confirmations": 3580,
        "size": 403750,
        "strippedsize": 403750,
        "weight": 1615000,
        "height": 0,
        "version": 1,
        "versionHex": "00000001",
        "merkleroot": "3426ccad3017e14a4ab6efddaa44cb31beca67a86c82f63de18705f1b6de88df",
        "tx": [
            "3426ccad3017e14a4ab6efddaa44cb31beca67a86c82f63de18705f1b6de88df"
        ],
        "time": 1570625829,
        "mediantime": 1570625829,
        "nonce": 709,
        "bits": "1f3fffff",
        "difficulty": 2.384149979653205e-07,
        "chainwork": "0000000000000000000000000000000000000000000000000000000000000400",
        "nextblockhash": "3fbdde4f2ccd683e4bae7d8867d1d647b21e5a90f3ae557c57e3f2b625d387d4",
        "txcount": 1
    },
    "error": null,
    "id": "api-server"
}
```

## /header/<string:hash>

This method return block header by given hash.

Params: none

Request: https://api.mbc.wiki/header/14c03ecf20edc9887fb98bf34b53809f063fc491e73f588961f764fac88ecbae

Responce:
```
{
    "result": {
        "hash": "14c03ecf20edc9887fb98bf34b53809f063fc491e73f588961f764fac88ecbae",
        "confirmations": 3623,
        "height": 0,
        "version": 1,
        "versionHex": "00000001",
        "merkleroot": "3426ccad3017e14a4ab6efddaa44cb31beca67a86c82f63de18705f1b6de88df",
        "time": 1570625829,
        "mediantime": 1570625829,
        "nonce": 709,
        "bits": "1f3fffff",
        "difficulty": 2.384149979653205e-07,
        "chainwork": "0000000000000000000000000000000000000000000000000000000000000400",
        "nextblockhash": "3fbdde4f2ccd683e4bae7d8867d1d647b21e5a90f3ae557c57e3f2b625d387d4",
        "txcount": 1
    },
    "error": null,
    "id": "api-server"
}
```

## /range/<int:height>

This method return range of blocks staring from certain height.

Params:
`offset`: number of blocks required (default: 30)

Request: https://api.mbc.wiki/range/100

Responce:
```
{
    "result": [
        {
            "hash": "4f99bb6f9640eb340c69a563b0f113c71481343f1e37b8e2f91107c02ba8c6e7",
            "minedhash": "0004110dad177766910aed21bfc511761172b0568d7ca2fdd86184bb3bd895f7",
            "confirmations": 3544,
            "strippedsize": 222,
            "size": 258,
            "weight": 924,
            "height": 100,
            "version": 536870912,
            "versionHex": "20000000",
            "merkleroot": "84cea323eaa44d5aed27f5f8b7a237298626865608ba4d947a95375ae9cb8649",
            "tx": [
                "84cea323eaa44d5aed27f5f8b7a237298626865608ba4d947a95375ae9cb8649"
            ],
            "time": 1570628802,
            "mediantime": 1570628799,
            "nonce": 452985008,
            "bits": "1f23bcba",
            "difficulty": 4.269654764157484e-07,
            "chainwork": "000000000000000000000000000000000000000000000000000000000001a3de",
            "previousblockhash": "a6248bb69a57e414bd109aff5db99ce1271e1fc34daac8fdc720fa714028f741",
            "nextblockhash": "1236eab5de3b26dd798021248101cccb5b8467b2406cd9703d8239e9fe4e7452",
            "txcount": 1,
            "nethash": 35
        },
        ...
    ],
    "error": null,
    "id": "api-server"
}
```

## /balance/<string:address>

This method return address balance.

Params: none

Request: https://api.mbc.wiki/balance/BfSf3YKJ84P2vhSYLZkTCJvAmDtZs79XBH

Responce:
```
{
    "result": {
        "balance": 127627708980,
        "received": 127627708980,
        "immature": 0
    },
    "error": null,
    "id": "api-server"
}
```

## /mempool/<string:address>

This method return address mempool transactions.

Params: none

Request: https://api.mbc.wiki/mempool/BfSf3YKJ84P2vhSYLZkTCJvAmDtZs79XBH

Responce:
```
{
    "result": {
        "tx": [
            {
                "txid": "2797000448842feed62a000f070615e3468211859d4ac3c34f19c8bd59c3fc69",
                "index": 0,
                "satoshis": 10000,
                "timestamp": 1570703951
            }
        ],
        "txcount": 1
    },
    "error": null,
    "id": "api-server"
}
```

## /unspent/<string:address>

This method return address unspent outputs.

Params:
`amount`: amount which you want to spend (default: 0 will return all utxos)

Request: https://api.mbc.wiki/unspent/BfSf3YKJ84P2vhSYLZkTCJvAmDtZs79XBH

Responce:
```
{
    "result": [
        {
            "txid": "3426ccad3017e14a4ab6efddaa44cb31beca67a86c82f63de18705f1b6de88df",
            "index": 5672,
            "script": "76a9147fd7e409fc303e407a933b3392aa197c66348da688ac",
            "value": 127627662980,
            "height": 0
        },
        ...
    ],
    "error": null,
    "id": "api-server"
}
```

## /history/<string:address>

This method return list of address transaction hashes.

Params:
`offset`: offset of transactions list (default: 0)

Request: https://api.mbc.wiki/history/BfSf3YKJ84P2vhSYLZkTCJvAmDtZs79XBH

Responce:
```
{
    "result": {
        "tx": [
            "279e770e469ffdfac463ec74f0a052fd546b249328d681cd58609760e9b57501",
            "957fc74933dcfc7da179bd53d01b2a7f8ffda4daa7a39b83656acf52ef772070",
            "cb844f6ee6dceb81a280e45ef65c0e965413bb43abb4285eb4c584aace4ec1c8",
            "f318418db0c56cb2735d1b2c581fa87311109216078efa57a0679fb0a47434d6",
            "d587f628cfb722b1eb590f07bd3b864b5c56b63bd6f4469a4e20024e2b9e2ed4",
            "2797000448842feed62a000f070615e3468211859d4ac3c34f19c8bd59c3fc69",
            "3426ccad3017e14a4ab6efddaa44cb31beca67a86c82f63de18705f1b6de88df"
        ],
        "txcount": 7
    },
    "error": null,
    "id": "api-server"
}
```

## /transaction/<string:hash>

This method return info about transaction.

Params: none

Request: https://api.mbc.wiki/transaction/957fc74933dcfc7da179bd53d01b2a7f8ffda4daa7a39b83656acf52ef772070

Responce:
```
{
    "result": {
        "txid": "957fc74933dcfc7da179bd53d01b2a7f8ffda4daa7a39b83656acf52ef772070",
        "hash": "957fc74933dcfc7da179bd53d01b2a7f8ffda4daa7a39b83656acf52ef772070",
        "version": 1,
        "size": 226,
        "vsize": 226,
        "weight": 904,
        "locktime": 0,
        "vin": [
            {
                "txid": "cb844f6ee6dceb81a280e45ef65c0e965413bb43abb4285eb4c584aace4ec1c8",
                "vout": 1,
                "scriptSig": {
                    "asm": "3045022100bcf51d6111d3f23a23689d1956e010433e4ea65a3680211e5e442e229ccedd59022049e89b4762788d1718ebc5f6c300d2a898f161f22e08a6a8e55b96fb55586522[ALL] 021121f5e63f7537a6c8e8881b0c54c5914cd117e775c3be0486205c45eced9117",
                    "hex": "483045022100bcf51d6111d3f23a23689d1956e010433e4ea65a3680211e5e442e229ccedd59022049e89b4762788d1718ebc5f6c300d2a898f161f22e08a6a8e55b96fb555865220121021121f5e63f7537a6c8e8881b0c54c5914cd117e775c3be0486205c45eced9117"
                },
                "sequence": 4294967293,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 436072406255f648da990ea1fa902cb98c4b6e20 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a914436072406255f648da990ea1fa902cb98c4b6e2088ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": [
                        "BZvwQt9vUebNsWJanWCJy3CGtqecuBDKU8"
                    ]
                },
                "value": 93000
            }
        ],
        "vout": [
            {
                "value": 1000,
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 7fd7e409fc303e407a933b3392aa197c66348da6 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a9147fd7e409fc303e407a933b3392aa197c66348da688ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": [
                        "BfSf3YKJ84P2vhSYLZkTCJvAmDtZs79XBH"
                    ]
                }
            },
            {
                "value": 91000,
                "n": 1,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 436072406255f648da990ea1fa902cb98c4b6e20 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a914436072406255f648da990ea1fa902cb98c4b6e2088ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": [
                        "BZvwQt9vUebNsWJanWCJy3CGtqecuBDKU8"
                    ]
                }
            }
        ],
        "hex": "0100000001c8c14eceaa84c5b45e28b4ab43bb1354960e5cf65ee480a281ebdce66e4f84cb010000006b483045022100bcf51d6111d3f23a23689d1956e010433e4ea65a3680211e5e442e229ccedd59022049e89b4762788d1718ebc5f6c300d2a898f161f22e08a6a8e55b96fb555865220121021121f5e63f7537a6c8e8881b0c54c5914cd117e775c3be0486205c45eced9117fdffffff02e8030000000000001976a9147fd7e409fc303e407a933b3392aa197c66348da688ac78630100000000001976a914436072406255f648da990ea1fa902cb98c4b6e2088ac00000000",
        "blockhash": "8b7ece31deca627b0ddd23eff3f0c580ab84ef8137921400f469bbcd40dc42a5",
        "confirmations": 1234,
        "time": 1570751006,
        "blocktime": 1570751006,
        "height": 2436,
        "amount": 92000
    },
    "error": null,
    "id": "api-server"
}
```

## /decode/<string:raw>

This method return decoded info about transaction.

Params: none

Request: https://api.mbc.wiki/decode/0100000001c8c14eceaa84c5b45e28b4ab43bb1354960e5cf65ee480a281ebdce66e4f84cb010000006b483045022100bcf51d6111d3f23a23689d1956e010433e4ea65a3680211e5e442e229ccedd59022049e89b4762788d1718ebc5f6c300d2a898f161f22e08a6a8e55b96fb555865220121021121f5e63f7537a6c8e8881b0c54c5914cd117e775c3be0486205c45eced9117fdffffff02e8030000000000001976a9147fd7e409fc303e407a933b3392aa197c66348da688ac78630100000000001976a914436072406255f648da990ea1fa902cb98c4b6e2088ac00000000

Responce:
```
{
    "result": {
        "txid": "957fc74933dcfc7da179bd53d01b2a7f8ffda4daa7a39b83656acf52ef772070",
        "hash": "957fc74933dcfc7da179bd53d01b2a7f8ffda4daa7a39b83656acf52ef772070",
        "version": 1,
        "size": 226,
        "vsize": 226,
        "weight": 904,
        "locktime": 0,
        "vin": [
            {
                "txid": "cb844f6ee6dceb81a280e45ef65c0e965413bb43abb4285eb4c584aace4ec1c8",
                "vout": 1,
                "scriptSig": {
                    "asm": "3045022100bcf51d6111d3f23a23689d1956e010433e4ea65a3680211e5e442e229ccedd59022049e89b4762788d1718ebc5f6c300d2a898f161f22e08a6a8e55b96fb55586522[ALL] 021121f5e63f7537a6c8e8881b0c54c5914cd117e775c3be0486205c45eced9117",
                    "hex": "483045022100bcf51d6111d3f23a23689d1956e010433e4ea65a3680211e5e442e229ccedd59022049e89b4762788d1718ebc5f6c300d2a898f161f22e08a6a8e55b96fb555865220121021121f5e63f7537a6c8e8881b0c54c5914cd117e775c3be0486205c45eced9117"
                },
                "sequence": 4294967293
            }
        ],
        "vout": [
            {
                "value": 0.1,
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 7fd7e409fc303e407a933b3392aa197c66348da6 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a9147fd7e409fc303e407a933b3392aa197c66348da688ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": [
                        "BfSf3YKJ84P2vhSYLZkTCJvAmDtZs79XBH"
                    ]
                }
            },
            {
                "value": 9.1,
                "n": 1,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 436072406255f648da990ea1fa902cb98c4b6e20 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a914436072406255f648da990ea1fa902cb98c4b6e2088ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": [
                        "BZvwQt9vUebNsWJanWCJy3CGtqecuBDKU8"
                    ]
                }
            }
        ]
    },
    "error": null,
    "id": "api-server"
}
```

## /mempool

This method return info about mempool.

Params: none

Request: https://api.mbc.wiki/mempool

Responce:
```
{
    "result": {
        "size": 0,
        "bytes": 0,
        "usage": 64,
        "maxmempool": 300000000,
        "mempoolminfee": 0.1,
        "minrelaytxfee": 0.1,
        "tx": []
    },
    "error": null,
    "id": "api-server"
}
```

## /supply

This method return info about current coins supply.

Params: none

Request: https://api.mbc.wiki/supply

Responce:
```
{
    "result": {
        "supply": 444065650592233,
        "height": 3675
    },
    "error": null,
    "id": "api-server"
}
```

## /fee

This method return recomended transaction fee.

Params: none

Request: https://api.mbc.wiki/fee

Responce:
```
{
    "result": {
        "feerate": 20045,
        "blocks": 6
    },
    "error": null,
    "id": "api-server"
}
```

## /broadcast

This methon broadcast raw signed transaction to MicroBitcoin network.
Keep in mind that you have to user **POST** request for this method!

Params:
`raw`: raw signed transaction

Request: https://api.mbc.wiki/broadcast
`raw`: `01000000010175b5e960976058cd81d62893246b54fd52a0f074ec63c4fafd9f460e779e27010000006b48304502210092ac0108461dec3d90c31781ccac868ebb876a2e09939793581d20d733369c6002207473120c0150e1777ee700da88b833ecfb1805cd629a18d29509fad0d03a97970121021121f5e63f7537a6c8e8881b0c54c5914cd117e775c3be0486205c45eced9117fdffffff0210270000000000001976a9147fd7e409fc303e407a933b3392aa197c66348da688ac880d0100000000001976a914436072406255f648da990ea1fa902cb98c4b6e2088ac00000000`

Responce:
```
{
    "result": "8d0f52a1177c7a954cf4f952532c49c8d55f9437539b544d92f83c14e1929950",
    "error": null,
    "id": "api-server"
}
```
