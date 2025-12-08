import redis

from utils.sys_config_reader import SysConfigReader
import logging

logger = logging.getLogger(__name__)


class RedisPoolManager:
    """
    Redis 连接池管理器，单例模式确保全局使用一个连接池
    """
    _instance = None
    _pool = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisPoolManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.init_pool()

    @classmethod
    def init_pool(cls):
        """
        初始化连接池
        """
        try:
            redis_conf = SysConfigReader().get_redis_config()
            conf_dict = {
                'host': redis_conf['host'],
                'port': redis_conf['port'],
                'db': 0,
                'password': redis_conf['passwd'],
                'decode_responses': True,
                'socket_timeout': 30,
                'max_connections': 20,
                'health_check_interval': 30
            }

            cls._pool = redis.ConnectionPool(**conf_dict)
            logger.info("Redis连接池初始化成功")
        except Exception as e:
            logger.error("Redis连接池初始化失败")
            raise e

    def get_client(self):
        if self._pool is None:
            self.init_pool()

        try:
            client = redis.Redis(connection_pool=self._pool)
            client.ping()
            return client
        except Exception as e:
            logger.warning("Redis Client 获取失败， 尝试重新初始化连接池")
            try:
                self.init_pool()
            except Exception as e:
                raise e
            return redis.Redis(connection_pool=self._pool)

    def close_pool(self):
        if self._pool:
            self._pool.close()


redis_pool_manager = RedisPoolManager()


def get_redis_client():
    return redis_pool_manager.get_client()