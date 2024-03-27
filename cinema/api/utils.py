from rest_framework.response import Response as RestResponse

class InvalidResponseDataValueError(Exception):
    def __str__(self):
        return "\033[91m" + str(self.args[0]) + "\033[0m"

class Response(RestResponse):
    def __init__(self, success=None, message=None, response=None,status=None):
        super().__init__(None, status=status)
        if success not in (True, False):
            raise InvalidResponseDataValueError("success value must be either True or False")
        if message is None:
            raise InvalidResponseDataValueError("message value cannot be None")
        if response is None:
            raise InvalidResponseDataValueError("response value cannot be None")
        if status is None:
            status = status.HTTP_200_OK
        
        data = {"success": success, "message": message, "response": response}
        self.data = data