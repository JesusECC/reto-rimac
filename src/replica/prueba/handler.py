from http import HTTPStatus
from api.responses import generate_response
def prueba(event, context):
    # data = os.environ.get('USER_POLL_ID')
    return generate_response('hola jesus',HTTPStatus.OK)
    