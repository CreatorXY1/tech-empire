import pytest

from app.core.config import get_database_url


def test_database_url_escapes_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_USER", "local-user")
    monkeypatch.setenv("DATABASE_PASSWORD", "p@ss:/word")

    url = get_database_url()

    assert url.drivername == "postgresql+psycopg"
    assert url.username == "local-user"
    assert url.password == "p@ss:/word"
    assert "p%40ss%3A%2Fword" in url.render_as_string(hide_password=False)


def test_database_url_requires_password(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_PASSWORD", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_PASSWORD is not configured"):
        get_database_url()


def test_database_port_must_be_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_PASSWORD", "configured")
    monkeypatch.setenv("DATABASE_PORT", "70000")

    with pytest.raises(RuntimeError, match="between 1 and 65535"):
        get_database_url()
