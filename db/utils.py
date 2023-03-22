from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

import sqlalchemy.orm as so
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import sessionmaker
from settings import Session



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





if __name__=="__main__":
    from settings import DatabaseSettings
    from tables import Articles

    kek=Articles(
            id=11,
            title='qwe',
            intro='asd',
            text='zxc',
            date='2023-03-21'
        )

    DatabaseSettings().setup_db()
    with create_session() as session:
        a=session.query(Articles).count()
        # a=session.query(Articles).all()
        print(a)
        # for i in a:
        #     print(i)
        # session.add(kek)