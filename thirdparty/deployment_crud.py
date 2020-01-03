from kubernetes import client
from kubernetes.client.rest import ApiException
from captain import settings
from utils.datetime_encode import DateEncoder
import json
from kubernetes.client.models.v1_deployment_status import V1DeploymentStatus
from kubernetes.client import Configuration
        # SSL/TLS verification
        # 将此设置为false可在从https服务器调用API时跳过验证SSL证书。
        #self.verify_ssl = True
        # 设置此选项可自定义证书文件以验证对等方。
        #self.ssl_ca_cert = None
        # 客户端证书文件
        #self.cert_file = None
        # 客户端密钥文件
        #self.key_file = None
        # 将其设置为True/False以启用/禁用SSL主机名验证。
        #self.assert_hostname = None


class DeploymentCrud(object):
    def __init__(self):
        token_file = settings.TOKEN_FILE
        ca_file = settings.CA_FILE
        with open(token_file, 'r') as file:
            token = file.read().strip('\n')
        k8s = settings.KUBERNETES
        configuration = client.Configuration()
        configuration.host = k8s
        configuration.verify_ssl = True
        configuration.ssl_ca_cert = ca_file
        configuration.api_key = {"authorization": "Bearer " + token}
        configuration.assert_hostname = settings.HOSTNAME
        client.Configuration.set_default(configuration)
        self.apps_v1 = client.AppsV1Api()

# ---------------------------------get deployment object or message-------------------------------------------------
    def get_deployment_status(self, deployment_name, namespace):
        result = dict()
        result['kind'] = 'Status'
        result['deployment_name'] = deployment_name
        result['namespace'] = namespace
        boolean, resp= self.get_deployment_object(deployment_name=deployment_name, namespace=namespace)
        if boolean:  #object
            data = resp.to_dict()
            data["code"] = "200"
            data = json.dumps(data,cls=DateEncoder)
            result['details'] = json.loads(data)
        else:        # 403/404
            result['details'] = json.loads(resp.body)
        return result

    def get_deployment_object(self, deployment_name, namespace): # return [boolean, object/exception]
        try:
            deployment = self.apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
            return True, deployment
        except ApiException as e:
            return False, e

# -----------------------------------create deployment message------------------------------------------------------
    def get_deployment_template(self, deployment_name, image, replicas):  # 获取模板
        # Configureate Pod template container
        container = client.V1Container(
            name=deployment_name,
            image=image,
            # command=['tail','-f','/dev/null'],
            ports=[client.V1ContainerPort(container_port=80)])
        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
            spec=client.V1PodSpec(containers=[container]))
        # Create the specification of deployment
        spec = client.V1DeploymentSpec(
            replicas=replicas,
            template=template,
            selector={'matchLabels': {'app': 'nginx'}})
        # Instantiate the deployment object
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name),
            spec=spec)

        return deployment


    def create_deployment(self, deployment_name, namespace, image, replicas):
        # Create deployement
        result = dict()
        result['kind'] = 'Create'
        result['deployment_name'] = deployment_name
        result['namespace'] = namespace
        boolean, resp = self.get_deployment_object(deployment_name=deployment_name, namespace=namespace)

        if boolean: # 已存在
            return self.get_deployment_status(deployment_name=deployment_name, namespace=namespace)
        elif resp.status == 404: # 不存在，则新建
            api_response = self.apps_v1.create_namespaced_deployment(
                body=self.get_deployment_template(deployment_name=deployment_name, image=image, replicas=replicas),
                namespace=namespace)
            data = api_response.to_dict()
            data["code"] = "200"
            data = json.dumps(data, cls=DateEncoder)
            result['details'] = json.loads(data)
            return result
        else: # 403 or 500 and so on
            result['details'] = json.loads(resp.body)
        return result

    def update_deployment(self, deployment_name, namespace, image=None, replicas=None):  # 更新镜像和副本
        # Update container image
        result = dict()
        result['kind'] = 'Update'
        result['deployment_name'] = deployment_name
        result['namespace'] =namespace

        boolean, resp = self.get_deployment_object(deployment_name=deployment_name, namespace=namespace)

        if boolean: # 找到目标
            if image and replicas:
                resp.spec.template.spec.containers[0].image = image
                resp.spec.replicas = replicas
            elif replicas:
                resp.spec.replicas = replicas
            elif image:
                resp.spec.template.spec.containers[0].image = image
            else:
                result['details'] = {"status":"Params not provides","code":101}
                return result
        # Update the deployment
            api_response = self.apps_v1.patch_namespaced_deployment(
                name=deployment_name,
                namespace="default",
                body=resp)

            data = api_response.status.to_dict()
            data["code"] = "200"
            data = json.dumps(data, cls=DateEncoder)
            result['details'] = json.loads(data)
            return result
        else:   # 没有该目标
            result['details'] = json.loads(resp.body)
            return result


    def delete_deployment(self, deployment_name, namespace):
        # Delete deployment
        boolean, resp = self.get_deployment_object(deployment_name=deployment_name, namespace=namespace)
        result = dict()
        result['kind'] = 'Delete'
        result['deployment_name'] = deployment_name
        result['namespace'] = namespace
        if boolean:
            self.apps_v1.delete_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=client.V1DeleteOptions(
                    propagation_policy='Foreground',
                    grace_period_seconds=5))
            data = resp.to_dict()
            data["code"] = "200"
            data = json.dumps(data, cls=DateEncoder)
            result['details'] = json.loads(data)
            return result
        else:        # 403/404
            result['details'] = json.loads(resp.body)
            return result






def main():

    deployment_name = "nginx-deployment"
    namespace = 'default'
    image = "nginx:1.12.0"
    replicas = 2
    dep = DeploymentCrud()
    print(dep.get_deployment_status())                        # 返回kind = Status
    # print(dep.create_deployment())                            # 存在kind = Status，不在kind = Create
    # print(dep.delete_deployment())                            # detail = [status,404,403]
    # print(dep.get_deployment_status())

    # print(dep.update_deployment(replicas=replicas))
    # dep.update_deployment_image(replicas)
    # update_deployment_replicas(apps_v1, deployment)

    # delete_deployment(apps_v1)


    # =======================================================================

    # get_deployment_status(apps_v1, deployment_name, namespace)

if __name__ == '__main__':
    main()
