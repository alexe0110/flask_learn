from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

import sqlalchemy.orm as so
from db import Session



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
