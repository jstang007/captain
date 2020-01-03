from django.http import JsonResponse
from thirdparty.deployment_crud import DeploymentCrud
from utils.response import CommonResponseMixin, ReturnCode
from django.views import View
from kubernetes.client.rest import ApiException
import json


class DeploymentView(View, CommonResponseMixin):
    def get(self, request):
        received_body = request.body
        message = None
        try:
            received_body = json.loads(received_body)
            args = received_body.get('args')
            dep = DeploymentCrud()
            data = dep.get_deployment_status(deployment_name=args.get('name'), namespace=args.get('namespace'))
        except (json.decoder.JSONDecodeError, ApiException, ValueError):
            data = ReturnCode.WRONG_PARAMS
            message = ReturnCode.message(data)

        data = self.wrap_json_response(data=data, message=message)
        return JsonResponse(data=data, safe=False, json_dumps_params={'ensure_ascii': False})



    def post(self, request):  # 新建，name+namespace+image+replicas必选
        received_body = request.body
        message = None
        try:
            received_body = json.loads(received_body)
            args = received_body.get('args')
            #for key, value in args.items():
            dep = DeploymentCrud()
            data = dep.create_deployment(deployment_name=args.get('name'), namespace=args.get('namespace'),
                                         image=args.get('image'), replicas=args.get('replicas'))
        except (json.decoder.JSONDecodeError, ApiException, ValueError):
            data = ReturnCode.WRONG_PARAMS
            message = ReturnCode.message(data)

        data = self.wrap_json_response(data=data, message=message)
        return JsonResponse(data=data, safe=False, json_dumps_params={'ensure_ascii': False})


    def put(self, request):  # 更新、修改
        received_body = request.body
        message = None
        try:
            received_body = json.loads(received_body)
            args = received_body.get('args')
            # # for key, value in args.items():
            dep = DeploymentCrud()
            data = dep.update_deployment(deployment_name=args.get('name'),namespace=args.get('namespace'),
                                         image=args.get('image'), replicas=args.get('replicas'))
        except (json.decoder.JSONDecodeError, ApiException, ValueError):
            data = ReturnCode.WRONG_PARAMS
            message = ReturnCode.message(data)

        data = self.wrap_json_response(data=data,message=message)
        return JsonResponse(data=data, safe=False, json_dumps_params={'ensure_ascii': False})

    def delete(self, request): # 删除
        received_body = request.body
        message = None
        try:
            received_body = json.loads(received_body)
            args = received_body.get('args')
            dep = DeploymentCrud()
            data = dep.delete_deployment(deployment_name=args.get('name'),namespace=args.get('namespace'))
        except (json.decoder.JSONDecodeError, ApiException, ValueError):
            data = ReturnCode.WRONG_PARAMS
            message = ReturnCode.message(data)

        data = self.wrap_json_response(data=data, message=message)
        return JsonResponse(data=data, safe=False, json_dumps_params={'ensure_ascii': False})
