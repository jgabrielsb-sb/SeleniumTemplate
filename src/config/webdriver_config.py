from core.models import dto_webdriver_config

from pathlib import Path

webdriver_config = dto_webdriver_config.WebdriverConfig(
    on_docker=False,
    will_perform_downloads=True,
    mode='local',
    default_download_path=Path('src/data/downloads')
)