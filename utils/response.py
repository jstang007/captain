class ReturnCode:
    SUCCESS = -200
    FAILED = -100
    RESOURCE_NOT_EXISTS = -404
    UNAUTHORIZED = -500
    BROKEN_AUTHORIZED_DATA = -501
    WRONG_PARAMS = -101

    @classmethod
    def message(cls, code):
        if code == cls.SUCCESS:
            return 'success'
        elif code == cls.FAILED:
            return 'failed'
        elif code == cls.UNAUTHORIZED:
            return 'unauthorized'
        elif code == cls.WRONG_PARAMS:
            return 'wrong params'
        elif code == cls.RESOURCE_NOT_EXISTS:
            return 'resource_not_exists'
        else:
            return ''

# Mixin模式，使用Mixin可通过继承类直接使用它的方法
class CommonResponseMixin(object):
    @classmethod
    def wrap_json_response(cls, data=None, code=None, message=None):
        response = {}
        if not code:
            code = ReturnCode.SUCCESS
        if not message:
            message = ReturnCode.message(code)
        if data:
            response['data'] = data

        response['result_code'] = code
        response['message'] = message
        return response