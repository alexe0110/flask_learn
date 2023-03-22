import socket
from typing import Any

from pydantic import BaseSettings
from sqlalchemy import engine_from_config
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapper, Query
from base import get_query_cls
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.exc import ArgumentError

Session = sessionmaker(query_cls=get_query_cls)

class SAUrl(URL):
    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> URL:
        try:
            return make_url(v)
        except ArgumentError as e:
            raise ValueError from e


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
        from tables import metadata

        engine = self.create_engine()
        metadata.bind = engine
        Session.configure(bind=engine)

    class Config:
        env_prefix = "BLOG_DB_"
