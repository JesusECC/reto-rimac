import json
# from boto3 import client
from .connect import Connect
class ConnectDB:
    
    data_cn = {
        "procedure": "",
        "args": [],
        "quantity_responses": 1,
        "cluster_name": "primate-migrate-ultimate-cluster"
    }
    
    def query(self, procedure, args=[], quantity_responses=1):
        self.clean_data()
        print('procedure')
        print(procedure)
        if quantity_responses > 1:
            self.data_cn['quantity_responses'] = quantity_responses
        self.data_cn['procedure'] = procedure
        self.data_cn['args'] = args

        response  = Connect.RdsConnect(json.dumps(self.data_cn))
        # lambda_client = client('lambda')
        # response = lambda_client.invoke(
        #     FunctionName = 'formula-app-back-dev-RdsConnect',
        #     Payload = json.dumps(self.data_cn)
        # )
        return response

    def clean_data(self):
        self.data_cn['quantity_responses'] = 1
        self.data_cn['procedure'] = ''
        self.data_cn['args'] = []