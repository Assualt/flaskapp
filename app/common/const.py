# Server
# PROJECT_NAME
PROJECT_NAME = "tsz"

# SQL EXEC Result
QUERY_FALED = "Query Failed"
QUERY_SUCCESS = "Query Success"
EXEC_SUCCESS = "Exec Success"
EXEC_FAILED = "Exec Failed"

# APP Status
APP_200_OK = 200
APP_300_BAD_RESULT = 300
APP_301_INVALID_ARGS = 301
APP_301_MESSAGE = "Invalid Args."
APP_302_UNSUPPORT_REQ_METHOD = 302
APP_302_MESSAGE = "Unsupported request method."
APP_400_BAD_REQUEST = 400
APP_400_MESSAGE = "Bad Request."
APP_403_UNRESOLVED_TYPE = 403
APP_403_MESSAGE = "UnResolved type."
APP_500_INTERNAL_ERROR = 500
APP_500_MESSAGE = "Internal error"

# HTTP STATUS
HTTP_200_OK = 200
HTTP_201_CREATE = 201
HTTP_300_MULTI_CHOICE = 300
HTTO_301_PERMANENT = 301
HTTP_400_BAD_REQUEST = 400
HTTP_401_AUTH_REQUIRED = 401
HTTP_403_FORBIDDENT = 403
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_408_REQ_TIMEOUT = 408
HTTP_410_GONE = 410
HTTP_500_INTERNAL_ERROR = 500
HTTP_502_BAD_GATEWAY = 502
HTTP_503_SVR_UNVALID = 503
HTTP_511_NET_AUTH_REQUIRED = 511

HTTP_200_MESSAGE = "Request OK."
HTTP_201_MESSAGE = "The request is created and new resources are created."
HTTP_300_MESSAGE = "Muti Choices"
HTTO_301_MESSAGE = "The requested page has been moved to a new URL."
HTTP_400_MESSAGE = "The server could not handle the request due to a syntax error."
HTTP_401_MESSAGE = "Authentication is required."
HTTP_403_MESSAGE = "The page you requested is forbidden."
HTTP_405_MESSAGE = "The method specified in the request is not allowed."
HTTP_408_MESSAGE = "Request Timeout."
HTTP_410_MESSAGE = "Server Gone."
HTTP_500_MESSAGE = "Server Internal Error."
HTTP_502_MESSAGE = "Bad GateWay."
HTTP_503_MESSAGE = "Service Unvaliable."
HTTP_511_MESSAGE = "Network Auth Required."


TSZ_MODEL_MYSQL = 10001
TSZ_MODEL_REDIS = 10002