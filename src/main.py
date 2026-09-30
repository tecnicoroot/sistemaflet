import flet as ft

from sistemaflet.core.config import get_settings


def main(page: ft.Page) -> None:
    settings = get_settings()
    page.title = settings.app_name
    page.add(
        ft.Text(f"{settings.app_name} ({settings.environment})", size=24),
    )


if __name__ == "__main__":
    ft.run(main)