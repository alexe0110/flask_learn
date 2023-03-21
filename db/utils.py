from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

import sqlalchemy.orm as so
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


@contextmanager
def create_session(**kwargs: Any) -> Iterator[so.Session]:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


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
