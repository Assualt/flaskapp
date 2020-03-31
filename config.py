import os
import configparser
from time import localtime, strftime
class config(object):
    def __init__(self, config_path):
        self.server_listen = ''
        self.server_port = 0
        self.server_debug_mode = False
        self.dbconfig = {}
        if not isinstance(config_path, str):
            raise ValueError("config path must be str")
        if config_path == '' or not os.path.exists(config_path):
            raise ValueError("config path is not exists {path}".format(path=config_path))
        self.reload_config(config_path)
        self.loggingLevel = ''
        self.loggingPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

        # login Time out Expire time
        self.expire_login_time = 3600 * 24

    def reload_config(self, config_path):
        print("Starting reloading config at time ", strftime("%Y-%m-%d %H:%M:%S", localtime()))
        try:
            parsed_config = configparser.ConfigParser()
            parsed_config.read(config_path)
        except Exception as e:
            print(" parsed config path {p} failed. errMsg:{err}".format(p=config_path, err=e))
            raise EnvironmentError("config path error.")
        # server
        self.server_listen = parsed_config.get('server', 'Listen', fallback='0.0.0.0')
        self.server_port = parsed_config.getint('server', 'Port', fallback=5000)
        self.server_debug_mode = True if parsed_config.get('server', 'RunTimeMode') == 'Debug' else False
        # database
        self.reaload_dbconfig(parsed_config)
        # logging
        self.loggingLevel = parsed_config.get('server', 'Log', fallback='Info')
        # expire time
        self.expire_login_time = parsed_config.getint('server', 'LoginExpireTime', fallback=3600 * 24)
        print("Finished reloading config at time ", strftime("%Y-%m-%d %H:%M:%S", localtime()))

    def reaload_dbconfig(self, parsed_config: configparser):
        """
        reload Database config
        :param parsed_config: config Object
        :return:
        """
        # mysql config
        mysql_host = parsed_config.get('mysql', 'Host', fallback='localhost')
        mysql_id = parsed_config.getint('mysql', 'ID')
        mysql_port = parsed_config.getint('mysql', 'Port', fallback=3306)
        mysql_user = parsed_config.get('mysql', 'User')
        mysql_passwd = parsed_config.get('mysql', 'Passwd')
        mysql_database = parsed_config.get('mysql', 'Database')
        mysql_charset = parsed_config.get('mysql', 'Charset')
        mysql_pool_size = parsed_config.getint('mysql', 'MaxPoolSize')

        # redis config
        redis_host = parsed_config.get('redis', 'Host', fallback='localhost')
        redis_id = parsed_config.getint('redis', 'ID')
        redis_port = parsed_config.getint('redis', 'Port')
        redis_passwd = parsed_config.get('redis', 'Passwd')
        redis_timeout = parsed_config.getint('redis', 'Timeout')

        self.dbconfig.__setitem__('mysql', config.to_formated_dbconfig(mysql_id, mysql_host, mysql_port, mysql_passwd,
                                                                       database=mysql_database, user=mysql_user, charset=mysql_charset,
                                                                       pool_size=mysql_pool_size))
        self.dbconfig.__setitem__('redis', config.to_formated_dbconfig(redis_id, redis_host, redis_port, redis_passwd, timeout=redis_timeout))

    @staticmethod
    def to_formated_dbconfig(id, host, port, passwd, database=None, user=None, charset='utf8', pool_size=10, timeout=10) -> dict:
        ret = {
            'id': id,
            'host': host,
            'port': port,
            'passwd': passwd,
            'charset': charset,
            'pool_size': pool_size,
            'timeout': timeout
        }
        ret.update({'user': user} if user else {})
        ret.update({'database': database} if database else {})
        return ret



file_path = os.path.dirname(os.path.abspath(__file__))
basic_config = config(os.path.join(file_path, "./conf/server.ini"))