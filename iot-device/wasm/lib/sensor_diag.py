from substrateinterface.contracts import ContractInstance, ContractExecutionReceipt
from substrateinterface import SubstrateInterface, Keypair
from scalecodec.type_registry import load_type_registry_file
from scalecodec.types import GenericContractExecResult

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

    def get_alert(self) -> GenericContractExecResult:
        return self.contractInstance.read(self.keypair, self.contract_method["get_alert"]["name"])

        
    def set_value(self, value) -> ContractExecutionReceipt:
        _ret = None
        
        # ==============================================================================
        # set argument
        # ==============================================================================
        contract_argument = self.contract_method["set"]["args"]
        contract_argument["value"] = value
        
        # ==============================================================================
        # check gas limit for contract call
        # ==============================================================================
        estimate_gas_result = self.contractInstance.read(self.keypair, self.contract_method["set"]["name"], args=contract_argument, value=0)

        if estimate_gas_result is not None:
            # ==============================================================================
            # success 
            # ==============================================================================
            bcolors.print_header("estimate gas\t:{}".format(estimate_gas_result.gas_required))

            # ==============================================================================
            # contract call
            # ==============================================================================
            bcolors.print_header("contract call\t:{}({})".format(self.contract_method["set"]["name"], contract_argument))
            _ret = self.contractInstance.exec(self.keypair, self.contract_method["set"]["name"], args=contract_argument, value=0, gas_limit=estimate_gas_result.gas_required)
        else:
            # ==============================================================================
            # failed
            # ==============================================================================
            bcolors.print_fail("contract read err")
            _ret = None

        return _ret


    def _set_arguments(self, args) -> bool:
        _ret = False

        # ==============================================================================
        # set arguments
        # ==============================================================================
        try:
            self.ws_url = args["ws_url"]
            self.type_registry_file_path = args["type_registry_file_path"]
            self.contract_metadata_json_file_path = args["contract"]["metadata_json_file_path"]
            self.contract_address = args["contract"]["address"]
            self.contract_executor_wallet_mnemonic = args["contract"]["executor_wallet_mnemonic"]
            self.contract_method = args["contract"]["method"]

            # done without a hitch.
            _ret = True
        except KeyError as e:
            bcolors.print_fail("require " + str(e) + " into args")

        return _ret

    def _prepaire_contract(self) -> bool:
        _ret = False

        # ==============================================================================
        # initialize substrate interface by arguments
        # ==============================================================================
        custom_type_registry = load_type_registry_file(self.type_registry_file_path)

        self.substrate = SubstrateInterface(
            url = self.ws_url,
            type_registry=custom_type_registry
        )
        # ==============================================================================
        # create keypair from mnemonic
        # ==============================================================================
        # dev account url https://docs.substrate.io/v3/tools/subkey/
        # keypair = Keypair.create_from_mnemonic(contract_executor_wallet_mnemonic)
        self.keypair = Keypair.create_from_uri(self.contract_executor_wallet_mnemonic)

        # ==============================================================================
        # Check if contract is on chain
        # ==============================================================================
        try:
            contract_info = self.substrate.query("Contracts", "ContractInfoOf", [self.contract_address])

            if contract_info.value:
                # ==============================================================================
                # found contract
                # ==============================================================================
                print('Found contract on chain: {contract_info.value}')
                self.contractInstance = ContractInstance.create_from_address(self.contract_address, self.contract_metadata_json_file_path, self.substrate)
                _ret = True

            else:
                # ==============================================================================
                # not found contract
                # ==============================================================================
                bcolors.print_fail('not found contract on chain')
        except ValueError as e:
            pass

        return _ret


if __name__ == "__main__":
    
    # ##############################################################################
    # default arguments
    # ==============================================================================
    args = dict()
    # TODO: please change
    args["ws_url"] = "ws://<your_local_node_address>:9944"
    args["type_registry_file_path"] = "./assets/my-custom-types.json"

    # ==============================================================================
    # contract
    # ==============================================================================
    args["contract"] = dict()
    args["contract"]["metadata_json_file_path"] = "./assets/sensor_diag.json"
    args["contract"]["address"] = "your_contract_address"
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

