from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

import app.database.session as database_session


def test_request_session_is_usable_and_closed_after_dependency_finishes(
    monkeypatch,
) -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    monkeypatch.setattr(database_session, "get_session_factory", lambda: factory)

    request_session: Generator[Session, None, None] = database_session.get_db_session()
    session = next(request_session)
    assert session.scalar(text("SELECT 1")) == 1
    assert session.in_transaction()

    request_session.close()

    assert not session.in_transaction()
    engine.dispose()
