import json
import logging

from user.models import User
from utils.redis_pool import get_redis_client
import system_global

logger = logging.getLogger(__name__)


def get_history_content(user):
    r_cli = get_redis_client()
    cache_history = r_cli.get(system_global.USER_HISTORY_CACHE_KEY % user.id) or "[]"
    user_history = json.loads(cache_history) or \
                    user.userchathistory_set.exists() and json.loads(user.userchathistory_set.first().content) or \
                    []
    logger.info("user_history:%s", user_history)
    return user_history if len(user_history) <= 10 else user_history[len(user_history) - 10:]


def completion_msg(history, question):
    history.append({"role": "system", "content": question})
    return history


def add_content_to_history(user: User, history, result):
    r_cli = get_redis_client()
    if not user:
        logger.error("add_content_to_history -- User not found")
        raise Exception("用户不存在")

    history.append({"role": "system", "content": result})

    user.userchathistory_set.update_or_create(user=user, defaults={"content": json.dumps(history)})
    r_cli.set(system_global.USER_HISTORY_CACHE_KEY % user.id, json.dumps(history), ex=3600)
