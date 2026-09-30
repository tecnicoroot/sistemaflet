#### Estrutura proposta

```
meu-app/
├── pyproject.toml
├── .env.example          # modelo versionado (o .env real fica no .gitignore)
├── src/
│   ├── main.py           # ponto de entrada do Flet
│   └── app/
│       ├── core/            # config (.env), logging, exceções
│       ├── domain/          # entidades e "ports" (interfaces)
│       ├── application/     # casos de uso: login, recuperar senha, 2FA
│       ├── infrastructure/  # implementações: repositórios, TOTP, e-mail
│       └── presentation/    # router, tema, responsividade, views, componentes
└── tests/
    ├── unit/
    └── integration/
```


#### Preparando o Ambiente
```bash
uv init meu-app --python 3.12
cd meu-app
uv init meu-app --python 3.12
cd meu-app
uv add "flet[all]"

uv run flet --version

uv add pydantic-settings pyotp
uv add --dev pytest pytest-cov ruff

```

no arquivo pyproject.toml
```toml
[tool.ruff]
line-length = 88
target-version = "py312"   # ajuste para o seu requires-python
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "N"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
addopts = "-ra --strict-markers"
```
criar .env.exemple
```ini
APP_NAME=Gestão de Robôs
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

no .gitignore
```
.pytest_cache/
.ruff_cache/
.coverage
```

src/sistemaflet/core/config.py
```python
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação, lidas de variáveis de ambiente e do .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Gestão de Robôs"
    environment: Literal["development", "testing", "production"] = "development"
    debug: bool = False
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

src/main.py
```python
import flet as ft

from app.core.config import get_settings


def main(page: ft.Page) -> None:
    settings = get_settings()
    page.title = settings.app_name
    page.add(
        ft.Text(f"{settings.app_name} ({settings.environment})", size=24),
    )


if __name__ == "__main__":
    ft.run(main)
```

tests/unit/test_config.py
```python
from app.core.config import Settings


def test_valores_padrao():
    settings = Settings(_env_file=None)
    assert settings.environment == "development"


def test_le_variaveis_de_ambiente(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Meu App")
    monkeypatch.setenv("ENVIRONMENT", "production")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Meu App"
    assert settings.environment == "production"
```

comandos:
```bash
uv run pytest                 # testes
uv run ruff check .           # lint
uv run ruff format .          # formatação
uv run flet run src/main.py   # abre o app desktop
```

#### Git

```
chore: inicializa projeto com uv e dependências
chore: configura ruff e pytest no pyproject.toml
feat(core): adiciona configurações via pydantic-settings e .env
feat: adiciona entrypoint flet com tela inicial
test(core): adiciona testes das configurações
```

|**Tipo** | **Quando usar**|
|---|---|
|**feat** | nova funcionalidade|
|**fix** | correção de bug|
|**chore** | tarefas de manutenção, dependências, config|
|**test** | criação ou ajuste de testes|
|**refactor** | mudança de código sem alterar comportamento|
|**docs** | documentação|
|**style** | formatação, sem mudar lógica|
|**ci** | pipelines e automações|

```bash
git init                      # se ainda não fez
git status                    # confirme que .env NÃO aparece na lista
uv run ruff check . && uv run ruff format . && uv run pytest
git add .
git commit -m "feat: estrutura inicial do projeto com flet, ruff, pytest e config via .env"

``` 