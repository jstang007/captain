from kubernetes import client
from kubernetes.client.rest import ApiException
from captain import settings
from utils.datetime_encode import DateEncoder
import json


class PodCrud(object):

    def __init__(self):
        token_file = settings.TOKEN_FILE
        ca_file = settings.CA_FILE
        with open(token_file, 'r') as file:
            Token = file.read().strip('\n')
        APISERVER = settings.KUBERNETES
        configuration = client.Configuration()
        configuration.host = APISERVER
        configuration.verify_ssl = True
        configuration.ssl_ca_cert = ca_file
        configuration.api_key = {"authorization": "Bearer " + Token}
        configuration.assert_hostname = settings.HOSTNAME
        client.Configuration.set_default(configuration)
        self.v1 = client.CoreV1Api()

    def get_target_pod(self, name, namespace):
        try:
            resp = self.v1.read_namespaced_pod(name=name, namespace=namespace)
            data = resp.to_dict()
            data = json.dumps(data,cls=DateEncoder)
            data = json.loads(data)
        except ApiException as e:
            data = json.loads(e.body)
        return data

    def delete_target_pod(self, name, namespace):
        try:
            self.v1.delete_namespaced_pod(name=name, namespace=namespace)
            result = dict()
            result['kind'] = 'DELETE'
            result['name'] = name
            result['namespace'] = namespace
            result['status'] = 'Success'
            result['code'] = 200
        except ApiException as e:
            result = json.loads(e.body)
        return result

    def list_all_pods_details(self, namespace):  # 返回pods json列表
        try:
            resp = self.v1.list_namespaced_pod(namespace=namespace)
            data = resp.to_dict()
            data = json.dumps(data, cls=DateEncoder)
            data = json.loads(data)
        except ApiException as e:
            data = json.loads(e.body)
        return data

    def list_all_pods_name(self, namespace):
        try:
            resp = self.v1.list_namespaced_pod(namespace=namespace)
            data = resp.to_dict()
            result = dict()
            result['kind'] = 'PodList'
            result['namespace'] = namespace
            temp = []
            data = json.dumps(data, cls=DateEncoder)
            dict_str = json.loads(data)
            for i in dict_str['items']:
                temp.append(i['metadata']['name'])
            result['items'] = temp
            result['status'] = 'Success'
            result['code'] = 200
        except ApiException as e:
            data = json.loads(e.body)
            return data
        return result