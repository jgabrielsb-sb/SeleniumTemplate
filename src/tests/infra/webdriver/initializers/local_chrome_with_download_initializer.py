
import pytest

from selenium import webdriver

from unittest.mock import patch

from selenium.webdriver.chrome.webdriver import WebDriver

from core.exceptions.webdriver_exceptions import (
    PreConditionNotMetException
)

from infra.webdriver.initializers import LocalChromeWithDownloadInitializer

from pathlib import Path

class TestLocalChromeWithDownloadInitializer:

    def test_if_raises_pre_condition_not_met_exception_when_download_path_does_not_exist(self):
        with pytest.raises(PreConditionNotMetException):
            LocalChromeWithDownloadInitializer(
                default_download_path=Path('non_existent_path')
            )

    def test_if_raises_when_download_path_exists_but_has_no_permission(self):
        download_path = Path("/fake/download/dir")

        with patch("os.path.exists", return_value=True), \
            patch("os.access", return_value=False):
        
            with pytest.raises(PreConditionNotMetException, match="does not have sufficient permissions"):
                LocalChromeWithDownloadInitializer(default_download_path=download_path)

    def test_if_verify_pre_conditions_raises_pre_condition_not_met_exception_when_pre_conditions_are_not_met(self):
        function_to_patch = 'infra.webdriver.initializers.LocalChromeWithDownloadInitializer._verify_if_download_path_exists'
        with patch(function_to_patch, side_effect=PreConditionNotMetException('test pre-condition not met')):
            with pytest.raises(PreConditionNotMetException, match="test pre-condition not met"):
                LocalChromeWithDownloadInitializer(default_download_path=Path('non_existent_path'))
    
    def test_if_get_config_returns_the_correct_config(self):
        function_to_patch_to_pass_pre_conditions = 'infra.webdriver.initializers.LocalChromeWithDownloadInitializer._verify_pre_conditions'
        with patch(function_to_patch_to_pass_pre_conditions, return_value=None):
            initializer = LocalChromeWithDownloadInitializer(default_download_path=Path('PATH TEST'))
            config = initializer._get_config()
            print(config.to_capabilities())

            assert isinstance(config, webdriver.ChromeOptions)
            assert config.to_capabilities()['goog:chromeOptions']['prefs']['download.default_directory'] == 'PATH TEST'
            assert config.to_capabilities()['goog:chromeOptions']['prefs']['download.prompt_for_download'] == False
            assert config.to_capabilities()['goog:chromeOptions']['prefs']['plugins.always_open_pdf_externally'] == True
    
    def test_if_get_webdriver_returns_the_correct_webdriver(self):
        function_to_patch_to_pass_pre_conditions = 'infra.webdriver.initializers.LocalChromeWithDownloadInitializer._verify_pre_conditions'
        with patch(function_to_patch_to_pass_pre_conditions, return_value=None):
            webdriver_instance = LocalChromeWithDownloadInitializer(default_download_path=Path('PATH TEST'))._get_webdriver()
            assert isinstance(webdriver_instance, webdriver.Chrome)

            


    