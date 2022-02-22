from flask import Flask, redirect, request, flash, url_for, render_template
from lib.sensor_diag import SensorDiag

import os

# ##############################################################################
# default arguments
# ==============================================================================
args = dict()
args["ws_url"] = "ws://host.docker.internal:9944"

# TODO: please change
args["publicKey"] = "metamask_public_key"
args["privateKey"] = "metamask_private_key"

args["type_registry_file_path"] = "./assets/my-custom-types.json"

# ==============================================================================
# contract
# ==============================================================================
args["contract"] = dict()
args["contract"]["metadata_json_file_path"] = "./assets/sensor_diag_abi.json"
args["contract"]["address"] = ""
args["contract"]["executor_wallet_mnemonic"] = "//Alice"

args["contract"]["method"] = dict()
args["contract"]["method"]["get_alert"] = dict()
args["contract"]["method"]["get_alert"]["name"] = "get_alert"
args["contract"]["method"]["get_alert"]["args"] = {}
args["contract"]["method"]["set"] = dict()
args["contract"]["method"]["set"]["name"] = "set"
args["contract"]["method"]["set"]["args"] = {"value":0}

# ##############################################################################

sensorDiag = None


app = Flask(__name__)
app.secret_key = os.urandom(24)
server_port = 8090

@app.route("/", methods=["GET", "POST"])
def index():
    global sensorDiag
    
    # コントラクトチェック
    if "" == args["contract"]["address"]:
        flash("最初にコントラクトアドレスを設定してください。")
        contract_status = "⛔"
    else:
        contract_status = "✅"
    
    if request.method == "POST":

        # value を設定するスマートコントラクトを実行
        sensorDiag.set_value(int(request.form["value"]))
        
        # alert を取得するスマートコントラクトを実行
        alert = sensorDiag.get_alert()

        flash("🎊 {}を送信しました。".format(request.form["value"]))
        flash("alertは {} です。".format(alert))

    return render_template('index.html', 
        contract_status=contract_status,
        contract_address=args["contract"]["address"]
    )

@app.route("/contract", methods=["POST"])
def contract_post():
    ret = ""
    global sensorDiag

    if "" != request.form["contract_address"]:
        args["contract"]["address"] = request.form["contract_address"]

        sensorDiag = SensorDiag()

        if sensorDiag.initialize(args):
            flash("コントラクトアドレスの設定に成功しました。")
            flash("contract address = {}".format(args["contract"]["address"]))
        else:
            flash("コントラクトアドレスの設定に失敗しました。")
            flash("コントラクトアドレスが正しいかチェックしてください。")
            flash("contract address = {}".format(args["contract"]["address"]))
            args["contract"]["address"] = ""

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run( host='0.0.0.0', port=server_port)