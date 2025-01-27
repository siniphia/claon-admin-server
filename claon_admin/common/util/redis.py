from dataclasses import asdict
from typing import Optional

from claon_admin.config.config import conf
from claon_admin.config.consts import REFRESH_TOKEN_EXPIRE_MINUTES
from claon_admin.config.redis import Redis

redis = Redis(host=asdict(conf())['REDIS_HOST'], port=asdict(conf())['REDIS_PORT'])


def save_refresh_token(refresh_token: str, user_id: str):
    with redis.get_connection() as conn:
        conn.set(refresh_token, user_id, ex=REFRESH_TOKEN_EXPIRE_MINUTES * 60)


def delete_refresh_token(refresh_token: str):
    with redis.get_connection() as conn:
        if conn.get(refresh_token) is not None:
            conn.delete(refresh_token)


def find_user_id_by_refresh_token(refresh_token: str) -> Optional[str]:
    with redis.get_connection() as conn:
        return conn.get(refresh_token)
