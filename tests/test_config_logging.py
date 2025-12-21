import logging
import os

import config.logging as logging_config
import config.settings as settings


def test_get_env_helpers(monkeypatch):
    monkeypatch.setenv("TEST_BOOL", "true")
    monkeypatch.setenv("TEST_INT", "5")
    monkeypatch.setenv("TEST_FLOAT", "1.5")
    monkeypatch.setenv("TEST_CSV", "a, b, c")

    assert settings._get_bool_env("TEST_BOOL", False) is True
    assert settings._get_int_env("TEST_INT", 1, min_value=1, max_value=10) == 5
    assert settings._get_float_env("TEST_FLOAT", 0.5, min_value=0.0, max_value=2.0) == 1.5
    assert settings._get_csv_env("TEST_CSV") == ["a", "b", "c"]


def test_configure_logging_stream_only(monkeypatch):
    monkeypatch.setattr(logging_config, "LOG_TO_FILE", False)
    logging_config.configure_logging()
    root_logger = logging.getLogger()
    assert root_logger.handlers


def test_configure_logging_file(tmp_path, monkeypatch):
    monkeypatch.setattr(logging_config, "LOG_TO_FILE", True)
    monkeypatch.setattr(logging_config, "LOG_DIR", str(tmp_path))
    monkeypatch.setattr(logging_config, "LOG_FILE_NAME", "app.log")
    monkeypatch.setattr(logging_config, "LOG_FILE_MAX_BYTES", 1024)
    monkeypatch.setattr(logging_config, "LOG_FILE_BACKUPS", 1)

    logging_config.configure_logging()
    logging.getLogger(__name__).info("log test")
    assert os.path.exists(tmp_path / "app.log")
