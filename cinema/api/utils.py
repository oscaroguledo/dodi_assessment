from ninja.responses import Response as NinjaResponse

class InvalidResponseDataError(Exception):
    def __str__(self):
        return "\033[91m" + str(self.args[0]) + "\033[0m"

class Response(NinjaResponse):
    def __init__(self, success=None, message=None, response=None, status=None):
        if success not in (True, False):
            raise InvalidResponseDataError("success value must be either True or False")
        if message is None:
            raise InvalidResponseDataError("message value cannot be None")
        if status is None:
            status = 200
        
        self.success = success
        self.message = message
        self.response = response
        self.status = status
        data = {"success": success, "message": message}
        if response:
            data['response']=response
        super().__init__(data, status=status)
