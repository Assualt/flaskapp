from app.common.const import *
class HttpResult(object):
    @staticmethod
    def format(code, message, app_code, app_message) -> dict:
        return {
                "status": code,
                "message": message,
                "info": {
                    "code": app_code,
                    "message": app_message
                }
        }

    @staticmethod
    def invalid_args() -> dict:
        return {
            "status": 200,
            "message": "Request OK",
            "info": {
                "code": 400,
                "message": "Invalid Args"
            }
        }

    @staticmethod
    def user_not_login() -> dict:
        return {
            "status": 200,
            "message": "Request OK",
            "info": {
                "code": 300,
                "message": "current User not logined."
            }
        }

    @staticmethod
    def unsupported_method() -> dict:
        return HttpResult.format(HTTP_405_METHOD_NOT_ALLOWED, HTTP_405_MESSAGE, APP_300_BAD_RESULT, "")

class DBResult(object):
    @staticmethod
    def format(model_id, status, info) -> dict:
        return {
            "modelID": model_id,
            "status": status,
            "result": info
        }


if __name__ == '__main__':
    print(HttpResult.format(200, "OK", "result", "OK"))
    print(DBResult.format(10001, "OK", None))