
import pytest
from core.models.dto_webdriver_config import WebdriverConfig
from pathlib import Path

class TestWebdriverConfig:
    def test_if_raises_error_when_on_docker_is_not_defined(self):
        with pytest.raises(ValueError):
            WebdriverConfig(
                on_docker=None,
                will_perform_downloads=True,
                mode='local',
                default_download_path=Path('~/Downloads')
            )

    def test_if_raises_error_when_will_perform_downloads_is_not_defined(self):
        with pytest.raises(ValueError):
            WebdriverConfig(
                on_docker=True,
                will_perform_downloads=None,
                mode='local',
                default_download_path=Path('~/Downloads')
            )

    def test_if_raises_error_when_mode_is_not_defined(self):
        with pytest.raises(ValueError):
            WebdriverConfig(
                on_docker=True,
                will_perform_downloads=True,
                mode=None,
                default_download_path=Path('~/Downloads')
            )

    def test_if_raises_error_when_default_download_path_is_not_valid(self):
        with pytest.raises(ValueError):
            WebdriverConfig(
                on_docker=True,
                will_perform_downloads=True,
                mode='INVALID MODE',
                default_download_path=Path('~/Downloads/')
            )

    def test_if_raises_error_when_default_download_path_is_not_defined_when_will_perform_downloads_is_true(self):
        with pytest.raises(ValueError):
            WebdriverConfig(
                on_docker=True,
                will_perform_downloads=True,
                mode='local',
                default_download_path=None
            )
            
            