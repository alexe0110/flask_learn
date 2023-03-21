import socket
from typing import Any

from pydantic import BaseSettings
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Engine

from db.utils import SAUrl


class BaseDBSettings(BaseSettings):
    url: SAUrl
    pool_recycle: int = 1
    pool_size: int = 1
    echo: bool
    application_name: str
    connection_timeout: int = 30
    pool_timeout: int = 5
    pool_pre_ping: bool = True
    connect_args: dict[str, Any] = {}
    query_cache_size: int = 1000

    def create_engine(self, **kwargs: Any) -> Engine:
        self.connect_args.setdefault("connect_timeout", self.connection_timeout)
        self.connect_args.setdefault("application_name", self.application_name)

        config = {
            "url": self.url,
            "echo": self.echo,
            "pool_recycle": self.pool_recycle,
            "pool_timeout": self.pool_timeout,
            "pool_pre_ping": self.pool_pre_ping,
            "pool_size": self.pool_size,
            "connect_args": self.connect_args,
            "query_cache_size": self.query_cache_size,
            **kwargs,
        }

        return engine_from_config(config, prefix="")


class DatabaseSettings(BaseDBSettings):
    echo: bool = True
    application_name = socket.gethostname()

    def setup_db(self) -> None:
        from db import metadata

        engine = self.create_engine()
        metadata.bind = engine

    class Config:
        env_prefix = "BLOG_DB_"
