from web3 import Web3
import json
import sys

# センサ値を受け取る！
value = int(sys.argv[1])

# デバイスの設定を読み込む！
deviceConfig = dict()
with open("./assets/device.json","r") as f:
    deviceConfig = json.load(f)

# Remix でデプロイしたスマートコントラクトの ABI を読み込む
# ※スマートコントラクトにどんな風にお願いいするかが書かれている。
abi = ""
with open(deviceConfig["contract"]["metadata_json_file_path"], "r") as f:
    abi = f.read()

# astar local node とお話しする用
w3 = Web3(Web3.WebsocketProvider('ws://{}:9944'.format(deviceConfig["nodeAddress"])))

# コントラクトインスタンスを作成
# コントラクトとお話しする用
address = deviceConfig["contract"]["address"]
contract_instance = w3.eth.contract(address=address, abi=abi)

# read state:
print(contract_instance.functions.get_value().call())

gas_estimate = contract_instance.functions.set(value).estimateGas()
print(gas_estimate)

nonce = w3.eth.get_transaction_count(deviceConfig["publicKey"])  
print(nonce)

_tx = {
    'gas': gas_estimate, 
    'gasPrice': Web3.toWei(1, 'gwei'),
    'nonce': nonce
}
tx_hash = contract_instance.functions.set(value).buildTransaction(_tx)
print(tx_hash)

private_key = deviceConfig["privateKey"]
signed_txn = w3.eth.account.sign_transaction(tx_hash, private_key=private_key)
print(signed_txn)

_ret_hex = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(_ret_hex)
