from sistemaflet.core.config import Settings


def test_valores_padrao():
    settings = Settings(_env_file=None)
    assert settings.environment == "development"


def test_le_variaveis_de_ambiente(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Meu App")
    monkeypatch.setenv("ENVIRONMENT", "production")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Meu App"
    assert settings.environment == "production"