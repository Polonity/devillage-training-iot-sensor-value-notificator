from web3 import Web3
import json

import random
from .bcolors import bcolors

class SensorDiag:
    
    def __init__(self):
        pass

    def initialize(self, args) -> bool:
        """class initializer

        Args:
            args (dict): arguments for substrateInterface

        Returns:
            bool: function status
        """
        _ret = False

        if False == self._set_arguments(args):
            pass
        elif False == self._prepaire_contract():
            pass
        else:
            _ret = True

        return _ret

    def get_alert(self):
        return self.contract_instance.functions.get_alert().call()

        
    def set_value(self, value) :
        _ret = None
        
        gas_estimate = self.contract_instance.functions.set(value).estimateGas()
        print(gas_estimate)

        nonce = self.w3.eth.get_transaction_count(self.publicKey)  
        print(nonce)

        _tx = {
            'gas': gas_estimate, 
            'gasPrice': Web3.toWei(1, 'gwei'),
            'nonce': nonce
        }
        tx_hash = self.contract_instance.functions.set(value).buildTransaction(_tx)
        print(tx_hash)

        private_key = self.privateKey
        signed_txn = self.w3.eth.account.sign_transaction(tx_hash, private_key=private_key)
        print(signed_txn)

        _ret_hex = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(_ret_hex)


        return _ret


    def _set_arguments(self, args) -> bool:
        _ret = False

        # ==============================================================================
        # set arguments
        # ==============================================================================
        try:
            self.ws_url = args["ws_url"]
            self.publicKey = args["publicKey"]
            self.privateKey = args["privateKey"]
            self.type_registry_file_path = args["type_registry_file_path"]
            self.contract_metadata_json_file_path = args["contract"]["metadata_json_file_path"]
            self.contract_address = args["contract"]["address"]

            # done without a hitch.
            _ret = True
        except KeyError as e:
            bcolors.print_fail("require " + str(e) + " into args")

        return _ret

    def _prepaire_contract(self) -> bool:
        _ret = False

        # Remix でデプロイしたスマートコントラクトの ABI を読み込む
        # ※スマートコントラクトにどんな風にお願いいするかが書かれている。
        abi = ""
        with open(self.contract_metadata_json_file_path, "r") as f:
            abi = f.read()

        # astar local node とお話しする用
        self.w3 = Web3(Web3.WebsocketProvider(self.ws_url))

        # コントラクトインスタンスを作成
        # コントラクトとお話しする用
        address = self.contract_address
        self.contract_instance = self.w3.eth.contract(address=address, abi=abi)

        _ret = True

        return _ret


if __name__ == "__main__":
    
    # ##############################################################################
    # default arguments
    # ==============================================================================
    args = dict()
    args["ws_url"] = "ws://host.docker.internal:9944"
    args["type_registry_file_path"] = "./assets/my-custom-types.json"

    # ==============================================================================
    # contract
    # ==============================================================================
    args["contract"] = dict()
    args["contract"]["metadata_json_file_path"] = "./assets/sensor_diag.json"
    args["contract"]["address"] = "aTzfYFfCTmSaV8cZVNmswkJjmaHppFk8qHmhZ9dW5GgN4Cy"
    args["contract"]["executor_wallet_mnemonic"] = "//Alice"

    args["contract"]["method"] = dict()
    args["contract"]["method"]["get_alert"] = dict()
    args["contract"]["method"]["get_alert"]["name"] = "get_alert"
    args["contract"]["method"]["get_alert"]["args"] = {}
    args["contract"]["method"]["set"] = dict()
    args["contract"]["method"]["set"]["name"] = "set"
    args["contract"]["method"]["set"]["args"] = {"value":0}

    # ##############################################################################

    sensorDiag = SensorDiag()

    if False == sensorDiag.initialize(args):
        exit(1)

    # ==============================================================================
    # get increment value
    # ==============================================================================
    get_result = sensorDiag.get_alert()
    if None != get_result:
        bcolors.print_green("read value\t:{}".format(get_result.contract_result_data))
    else:
        bcolors.print_fail("contract err")
        exit(1)

    # ==============================================================================
    # set value
    # ==============================================================================
    get_result = sensorDiag.set_value(random.randint(1, 20))
    if get_result.is_success:
        bcolors.print_green("exec success\t:" + str(get_result.contract_events))
    else:
        bcolors.print_fail(get_result.error_message)
        
    # ==============================================================================
    # get increment value
    # ==============================================================================
    get_result = sensorDiag.get_alert()
    if None != get_result:
        bcolors.print_green("read value\t:{}".format(get_result.contract_result_data))
    else:
        bcolors.print_fail("contract read err")
        exit(1)

