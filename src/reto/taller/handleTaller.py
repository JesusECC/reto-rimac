from http import HTTPStatus
from api.responses import generate_response, generate_response_db, generate_response_error_db
import json
from libs.service_database import ConnectDB
connect = ConnectDB()
def getTipoTaller(event, context):
    data = connect.query("sp_getTipoTaller")
    print('********************************')
    print(data)
    if data[0].get("error") is not None:
        return generate_response_error_db(data[0].get("message","Error"),HTTPStatus.OK)
    return generate_response(data, HTTPStatus.OK)

def findTaller(event, context):
    params = json.loads(event["body"])
    idDistrito = params["distrito"]
    idTaller = params["tipo"]
    idPlaca = params["placa"]

    data = connect.query("sp_getTaller",[idDistrito,idTaller,idPlaca])
    print('********************************')
    print(data)
    if data[0].get("error") is not None:
        return generate_response_error_db(data[0].get("message","Error"),HTTPStatus.OK)
    return generate_response(data, HTTPStatus.OK)
