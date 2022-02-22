from lib.sensor_diag import SensorDiag
from lib.bcolors import bcolors

import json                     # for parsing device.json

class SensorNotify:
    def __init__(self):
        pass
        
    # ##############################################################################
    def initialize(self, args) -> bool:
        _ret = False
        self.sensorDiag = SensorDiag()

        if self.sensorDiag.initialize(args):
            bcolors.print_header("コントラクトアドレスの設定に成功しました。")
            bcolors.print_header("contract address = {}".format(args["contract"]["address"]))
            _ret = True
        else:
            bcolors.print_fail("コントラクトアドレスの設定に失敗しました。")
            bcolors.print_fail("コントラクトアドレスが正しいかチェックしてください。")
            bcolors.print_fail("contract address = {}".format(args["contract"]["address"]))
            _ret = False
        
        return _ret

    def sensor_notify(self, _value) -> bool:
        _ret = False
        # ##############################################################################
        # get sensor value from sensor
        # ##############################################################################
        # value を設定するスマートコントラクトを実行
        get_result = self.sensorDiag.set_value(_value)
        if get_result.is_success:
            bcolors.print_green("exec success\t:" + str(get_result.contract_events))
            _ret = True
        else:
            bcolors.print_fail(get_result.error_message)
            _ret = False
            
        return _ret

    def get_sensor_value(self) -> int:
        return 1234

def _device_config(_path):
    with open(_path,"r") as f:
        _device_config = json.load(f)
        return _device_config



def _configure() -> dict:
    # ##############################################################################
    # default arguments
    # ==============================================================================
    args = dict()
    # TODO: please change
    args["ws_url"] = "ws://<your_local_node_address>:9944"
    args["type_registry_file_path"] = "./assets/my-custom-types.json"
    args["device_config_file_path"] = "./assets/device.json"

    # ==============================================================================
    # contract
    # ==============================================================================
    args |= _device_config(args["device_config_file_path"])

    # ==============================================================================

    return args

if __name__ == "__main__":
    args = _configure()
    sensorNotify = SensorNotify()
    if sensorNotify.initialize(args):
        value = sensorNotify.get_sensor_value()
        sensorNotify.sensor_notify(value)
