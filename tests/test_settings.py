from config.settings import validate_settings


def test_validate_settings_has_no_errors():
    issues = validate_settings()
    assert issues["errors"] == []
