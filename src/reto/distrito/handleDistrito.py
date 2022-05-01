from http import HTTPStatus
from api.responses import generate_response, generate_response_db, generate_response_error_db
from libs.service_database import ConnectDB
connect = ConnectDB()

def listaDistrito(event, context):
    data = connect.query("sp_getListDistrito")
    print('********************************')
    print(data)
    if data[0].get("error") is not None:
        return generate_response_error_db(data[0].get("message","Error"),HTTPStatus.OK)
    return generate_response(data, HTTPStatus.OK)