import json
from http import HTTPStatus
# "Content-Type": "application/json",
    #         "Access-Control-Allow-Origin": "*"
cors_headers = { 
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Office, User, X-PINGOTHER, Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With',
    'Access-Control-Allow-Methods': 'POST, PUT, GET, OPTIONS'
}

def generate_empty_response(status_code):
    return {
        'headers': cors_headers,
        'statusCode': status_code
    }

def generate(body=None,message=None,error=False,success=True):
    return json.dumps({"success": success, 
            "message":message, 
            "data": body,
            "error":error,})



def generate_response(body, status_code):
    response = generate_empty_response(status_code)
    response['body'] = generate(body)
    return response

def generate_response_db(message,status_code) :
    response = generate_empty_response(status_code)
    response['body'] = generate(None,message)
    return response

def generate_response_error_db(message,status_code) :
    response = generate_empty_response(status_code)
    response['body'] = generate(None,message,True,False)
    return response