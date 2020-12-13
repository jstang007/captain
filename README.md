# caption


### Description  
Kubernetes(K8s)API接口调用示例, 本人用于容器服务弹性伸缩(结合Prometheus+Altermanager)  


### Require
- Docker
- kubelet1.14.0(>=1.14.0)
- kubectl1.14.0(>=1.14.0)
- kubeadm1.14.0(>=1.14.0)
- Python3.7(>=3.6.0)

### RBAC Auth
[What RBAC? K8s-RBAC入门(本人文章)](https://blog.csdn.net/qq_38900565/article/details/102585741)  
使用K8s的API需要namesapce+toekn  
为了简单起见，使用超级管理员的权限，其他权限设定可根据K8s文档的RBAC认证进行设置，这里不做过多阐述。  
1.采用集群角色的权限：cluster-admin  
2.创建集群角色绑定： ClusterRoleBinding 和 创建服务账户: ServiceAccount  
cat k8s-admin.yaml  
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-admin
  namespace: kube-system
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: api-admin
subjects:
  - kind: ServiceAccount
    name: api-admin
    namespace: kube-system
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```
执行创建: 
kubectl create -f k8s-admin.yaml
获取服务账户的token名：
kubectl describe sa -n kube-system api-admin | grep ^Tokens
>Tokens:              api-admin-token-xxxxx
根据token获取令牌
[root@k8s-master k8s]# kubectl describe secret dashboard-admin-token-xxxxx -n kube-system | grep ^token
token:      eyJhbGciOiJSUzI1NiIsI......f2NkjH0YsBD7QEjRiQxp0Cv35rHC0pXuyRtDDKM7VE_RppJoY06WCRzAwZGCOBE1H6A
3.保存token
4.指定操作的命名空间: echo 'default' > namespace
综上所述拿到了namespace和token.(./resources/authority)

### Usage
python manage.py runserver 0.0.0.0:8800
