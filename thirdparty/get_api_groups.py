from kubernetes import client, watch
from kubernetes.client.rest import ApiException
import os
from captain import settings


def get_target_pod(v1, name, namespace):  # 返回json yaml文件
    name = name
    resp = None
    try:
        resp = v1.read_namespaced_pod(name=name, namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)
    print(resp)
    return True
def delete_target_pod(v1, name, namespace):  # 先找到，再删除
    if not get_target_pod(v1, name, namespace):
        print('name<%s> not fount' % name)
        return False

    return True



def list_all_pod(v1):
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for item in ret.items:
        print("%s\t%s\t%s" % (item.status.pod_ip, item.metadata.namespace, item.metadata.name))


def get_api_groups(v1):
    count = 10
    w = watch.Watch()
    for event in w.stream(v1.list_namespace, _request_timeout=60):
        print("Event: %s %s" % (event['type'], event['object'].metadata.name))
        count -= 1
        if not count:
            w.stop()
    print('Ended.')


def main():
    token_file = os.path.join(settings.TOKEN_DIR, 'token2.txt')
    with open(token_file, 'r') as file:
        Token = file.read().strip('\n')

    APISERVER = 'https://172.31.50.134:6443'
    configuration = client.Configuration()
    configuration.host = APISERVER
    configuration.verify_ssl = False
    configuration.api_key = {"authorization": "Bearer " + Token}
    client.Configuration.set_default(configuration)

    v1 = client.CoreV1Api()
    # get_api_groups(v1)  # 监控域名
    # list_all_pod(v1) # 列出所有pod名、ip、域名空间
    get_target_pod(v1, 'centos', 'default') # 获取指定
    # delete_target_pod(v1, 'centos', "default")

if __name__ == '__main__':
    main()