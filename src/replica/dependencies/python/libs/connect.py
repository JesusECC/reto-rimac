from api.responses import generate_response_error_db
import json
import os
import pymysql


class Connect:
    def RdsConnect(data):
        """
        request example
        {
            "procedure": "wdms_2020.sp_get_marcaciones_fecha",
            "args": [
                "2020-12-30"
            ],
            "quantity_responses": 1,
            "cluster_name": "primate-migrate-ultimate-cluster"
        }
        """
        try:
            event = json.loads(data)
            event['procedure'] = event.get('procedure', '')
            event['args'] = event.get('args', '')
            event['query'] = event.get('query', '')
            event['quantity_responses'] = event.get('quantity_responses', 1)
            # event['procedure'] = event.get('procedure', '')
            # event['args'] = event.get('args', '')
            # event['query'] = event.get('query', '')
            # event['quantity_responses'] = event.get('quantity_responses', 1)

            conv = pymysql.converters.conversions.copy()
            conv[7] = str       # convert datetimes to strings
            conv[10] = str       # convert date to strings
            conv[11] = str       # convert timedelta to strings
            conv[12] = str       # convert datetime to strings
            conv[246] = float       # convert deci    mal to float

            # dsn = {
            #     'primate-migrate-ultimate-cluster': {
            #         'db': 'formula_ac_dev',
            #         'user': 'admin',
            #         'passwd': 'RNH7uRvBuTodj^7**',
            #         'w': 'formula-ac.chfcjyb9o5c3.us-east-1.rds.amazonaws.com',
            #         'r': 'formula-ac.chfcjyb9o5c3.us-east-1.rds.amazonaws.com'
            #     }
            # }
            dsn = {
                'primate-migrate-ultimate-cluster': {
                    'db': os.environ.get('DB'),
                    'user': os.environ.get('USER'),
                    'passwd': os.environ.get('PASSWORD'),
                    'w': os.environ.get('WRITER'),
                    'r': os.environ.get('READER'),
                }
            }
            event['cluster_name'] = event['cluster_name'] if 'cluster_name' in event and event[
                'cluster_name'] in dsn else 'primate-migrate-ultimate-cluster'
            results = []
            instance = dsn[event['cluster_name']]['r' if event['procedure'].split(
                '.')[-1][0:6] == 'sp_get' else 'w']
            conn = pymysql.connect(
                db=dsn[event['cluster_name']]['db'],
                user=dsn[event['cluster_name']]['user'],
                passwd=dsn[event['cluster_name']]['passwd'],
                host=instance,
                charset='utf8',
                conv=conv
            )
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            if event['procedure'] != '':
                print('Consultando BD: Cluster:', event['cluster_name'],
                      'procedure:', event['procedure'], ' args: ', event['args'])
                cursor.callproc(event['procedure'], event['args'])

            else:
                print('Consultando BD: Cluster:',
                      event['cluster_name'], 'query:', event['query'])
                cursor.execute(event['query'])

            if event['quantity_responses'] == 1:
                results = cursor.fetchall()

            else:
                results = []
                for x in range(event['quantity_responses']):
                    if x > 0:
                        cursor.nextset()
                    results.append(cursor.fetchall())

            conn.commit()
            cursor.close()
            conn.close()

            # responses = {
            #     'data': results,
            # }

            return results
        except pymysql.err.OperationalError as err:
            return {"error": True, "message": str(err)}

        except pymysql.err.DataError as err:
            return {"error": True, "message": str(err)}
