
"""
 A Flask App For TSZ Backup Server
@Author:
@Date:
@Version:
@Description:
"""

from datetime import datetime
from functools import update_wrapper
__author__ = 'xhou'

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import basic_config as api_config
app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    CORS(app)
    app.run(host=api_config.server_listen, port=api_config.server_port, debug=api_config.server_debug_mode)