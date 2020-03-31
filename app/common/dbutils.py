import datetime
import time

import pymysql
import redis
from DBUtils.PooledDB import PooledDB

from app.common.commresult import *
from config import basic_config as conf
from logger import file_logger as logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

DB_CONFIG = {
    'host': conf.dbconfig['mysql']['host'],
    'port': conf.dbconfig['mysql']['port'],
    'user': conf.dbconfig['mysql']['user'],
    'passwd': conf.dbconfig['mysql']['passwd'],
    'db': conf.dbconfig['mysql']['database'],
    'charset': conf.dbconfig['mysql']['charset'],
    'maxconn': conf.dbconfig['mysql']['pool_size']
}
ORM_ENGINE = "mysql+pymysql://{user}:{passwod}@{host}:{port}/{database}?charset={charset}".format(
    user=DB_CONFIG['user'],
    passwod=DB_CONFIG['passwd'],
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    database=DB_CONFIG['db'],
    charset=DB_CONFIG['charset'])


class MysqlHelper(object):
    """
    mysql工具类,实现数据连操作,实现正常的增删改查功能
    """
    _pool_db = None

    def __init__(self):
        self._conn = MysqlHelper.get_connection()
        self._cursor = self._conn.cursor()
        pass

    @staticmethod
    def get_connection():
        global _pool_db
        if MysqlHelper._pool_db is None:
            _pool_db = PooledDB(pymysql, DB_CONFIG['maxconn'], host=DB_CONFIG['host'], user=DB_CONFIG['user'],
                                passwd=DB_CONFIG['passwd'], db=DB_CONFIG['db'], port=DB_CONFIG['port'],
                                charset=DB_CONFIG['charset'])
        return _pool_db.connection()

    def query(self, sql, param=None) -> dict:
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count:
                result = self._cursor.fetchall()
                return DBResult.format(TSZ_MODEL_MYSQL, QUERY_SUCCESS, result)
            return DBResult.format(TSZ_MODEL_MYSQL, QUERY_FALED, None)
        except Exception as e:
            return DBResult.format(TSZ_MODEL_MYSQL, QUERY_FALED,
                                   "Catch Exception in MysqlHelper.query {e}".format(e=e))

    def insert(self, sql: str, param=None) -> dict:
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            self._conn.commit()
            if count:
                return DBResult.format(TSZ_MODEL_MYSQL, EXEC_SUCCESS, None)
            return DBResult.format(TSZ_MODEL_MYSQL, EXEC_FAILED, None)
        except Exception as e:
            return DBResult.format(TSZ_MODEL_MYSQL, EXEC_FAILED,
                                   "Catch Exception in MysqlHelper.insert {e}".format(e=e))

    def update(self, sql: str, param=None) -> dict:
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            self._conn.commit()
            if count:
                return DBResult.format(TSZ_MODEL_MYSQL, EXEC_SUCCESS, None)
            return DBResult.format(TSZ_MODEL_MYSQL, EXEC_FAILED, None)
        except Exception as e:
            return DBResult.format(TSZ_MODEL_MYSQL, EXEC_FAILED,
                                   "Catch Exception in MysqlHelper.query {e}".format(e=e))
        pass


_redis_pool = None


def get_redis():
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.ConnectionPool(host=conf.dbconfig['redis']['host'], port=conf.dbconfig['redis']['port'],
                                           password=conf.dbconfig['redis']['passwd'])
        if _redis_pool:
            logger.info("connect Redis Server %s:%s ok", conf.dbconfig['redis']['host'], conf.dbconfig['redis']['port'])
        else:
            logger.info("connect Redis Server %s:%s failed", conf.dbconfig['redis']['host'],
                        conf.dbconfig['redis']['port'])
    return redis.Redis(connection_pool=_redis_pool, socket_timeout=conf.dbconfig['redis']['timeout'])


class RedisHelper(object):
    @staticmethod
    def setX(key, val, expire_time=3600 * 24) -> dict:
        try:
            redis_cli = get_redis()
            if not redis_cli:
                logger.info(" redis_cli is None")
            if redis_cli.set(key, val):
                redis_cli.expire(key, expire_time)
                logger.info("set %s expiretime:%s", key,
                            datetime.datetime.fromtimestamp(int(time.time()) + expire_time))
                return DBResult.format(TSZ_MODEL_REDIS, EXEC_SUCCESS, None)
            else:
                logger.info("set %s into redis failed", key)
                return DBResult.format(TSZ_MODEL_REDIS, EXEC_FAILED, None)
        except Exception as e:
            errmsg = "Catch Execption in Redis setX({key},{val}). ErrMsg:{msg}".format(key=key, val=val, msg=e)
            logger.warning(errmsg)
            return DBResult.format(TSZ_MODEL_REDIS, EXEC_FAILED, errmsg)

    @staticmethod
    def delX(key) -> dict:
        try:
            redis_cli = get_redis()
            redis_cli.delete(key)
            return DBResult.format(TSZ_MODEL_REDIS, EXEC_SUCCESS, None)
        except Exception as e:
            errmsg = "Catch Execption in Redis getX({key}). ErrMsg:{msg}".format(key=key, msg=e)
            logger.warning(errmsg)
            return DBResult.format(TSZ_MODEL_REDIS, EXEC_FAILED, errmsg)
        pass

    @staticmethod
    def getX(key, expire_time=3600 * 24, update=False) -> dict:
        try:
            redis_cli = get_redis()
            val = redis_cli.get(key)
            if val and update:
                redis_cli.expire(key, expire_time)
                logger.debug("update to set % expiretime:%", key,
                             datetime.datetime.fromtimestamp(int(time.time()) + expire_time))
            if val:
                return DBResult.format(TSZ_MODEL_REDIS, QUERY_SUCCESS, val.decode())
            else:
                return DBResult.format(TSZ_MODEL_REDIS, QUERY_SUCCESS, val)
        except Exception as e:
            errmsg = "Catch Execption in Redis getX({key}). ErrMsg:{msg}".format(key=key, msg=e)
            logger.warning(errmsg)
            return DBResult.format(TSZ_MODEL_REDIS, QUERY_FALED, errmsg)


# ORM ENGINE
engine = None
def getSession() -> Session:
    global engine
    try:
        if engine is None:
            engine = create_engine(ORM_ENGINE)
        Session = sessionmaker(engine)
        return True, Session()
    except Exception as e:
        logger.warning("get Session from Engine Failed %s", e)
    return False, None


if __name__ == '__main__':
    from app.mapping.dborm import *

    t = TSZAuth(uid=1, uname='xhou', uauthkey='123456', udesc='', uorgid='1', utel='13833211231', uemail='xhou@pp.com')
    flag, db_session = getSession()
    rows = db_session.query(TSZAuth).all()

    for row in rows:
        print(row, row.__dict__)

    db_session.commit()
    db_session.close()

    #
    # RedisHelper.setX("Redis", "Test", 5)
    # logger.info("get key:{val} currentTime:{t1}".format(val=RedisHelper.getX("Redis", 5),
    #                                                     t1=datetime.datetime.fromtimestamp(int(time.time()))))
    # time.sleep(3)
    # logger.info("get key:{val} currentTime:{t1}".format(val=RedisHelper.getX("Redis", 5),
    #                                                     t1=datetime.datetime.fromtimestamp(int(time.time()))))
    # time.sleep(5)
    # logger.info("get key:{val} currentTime:{t1}".format(val=RedisHelper.getX("Redis", 5),
    #                                                     t1=datetime.datetime.fromtimestamp(int(time.time()))))
    # RedisHelper.delX("Redis")
