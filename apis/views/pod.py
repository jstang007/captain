from django.http import JsonResponse
from thirdparty.pod_crud import PodCrud
from utils.response import CommonResponseMixin
from kubernetes.client.rest import ApiException
from django.views import View
import json
from utils.response import ReturnCode


class PodView(View, CommonResponseMixin):

    def post(self, request):
        received_body = request.body
        message = None
        try:
            received_body = json.loads(received_body)
            args = received_body.get('args')
            pc = PodCrud()
            data = pc.get_target_pod(name=args.get('name'), namespace=args.get('namespace'))
        except (json.decoder.JSONDecodeError, ApiException, ValueError):
            data = ReturnCode.WRONG_PARAMS
            message = ReturnCode.message(data)

        data = self.wrap_json_response(data=data, message=message)
        return JsonResponse(data=data, safe=False, json_dumps_params={'ensure_ascii': False})

    def delete(self, request):
        received_body = request.body
        message = None
        try:
            received_body = json.loads(received_body)
            args = received_body.get('args')
            pc = PodCrud()
            data = pc.delete_target_pod(name=args.get('name'), namespace=args.get('namespace'))
        except (json.decoder.JSONDecodeError, ApiException, ValueError):
            data = ReturnCode.WRONG_PARAMS
            message = ReturnCode.message(data)

        data = self.wrap_json_response(data=data, message=message)
        return JsonResponse(data=data, safe=False, json_dumps_params={'ensure_ascii': False})