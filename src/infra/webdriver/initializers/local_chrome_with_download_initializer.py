
from selenium import webdriver

import os

from pathlib import Path

from core.exceptions.webdriver_exceptions import (
    PreConditionNotMetException,
)

from infra.webdriver.base_selenium_initializer import SeleniumInitializer

from infra.logger import get_logger

logger = get_logger('infra.webdriver.initializers.local_chrome_with_download_initializer')


class LocalChromeWithDownloadInitializer(SeleniumInitializer):
    def __init__(self, default_download_path: Path):
        if not isinstance(default_download_path, Path):
            MESSAGE_ERROR = f'default_download_path must be a Path object'
            logger.error(MESSAGE_ERROR, exc_info=True)
            raise ValueError(MESSAGE_ERROR)
        
        self.default_download_path = default_download_path
        super().__init__()
    
    def _verify_if_download_path_exists(self):
        download_path = self.default_download_path
        if not os.path.exists(download_path):
            MESSAGE_ERROR = f'download_path {download_path} does not exist'
            logger.error(MESSAGE_ERROR, exc_info=True)
            raise PreConditionNotMetException(MESSAGE_ERROR)
    
    def _verify_if_download_path_has_sufficient_permissions(self):
        download_path = self.default_download_path
        if os.path.exists(download_path) and not os.access(download_path, os.W_OK):
            MESSAGE_ERROR = f'download_path {download_path} does not have sufficient permissions'
            logger.error(MESSAGE_ERROR, exc_info=True)
            raise PreConditionNotMetException(MESSAGE_ERROR)
    
    def _verify_pre_conditions(self):
        pre_conditions = [
            self._verify_if_download_path_exists,
            self._verify_if_download_path_has_sufficient_permissions
        ]

        pre_conditions_not_met = []
        
        for pre_condition in pre_conditions:
            try:
                pre_condition()
            except PreConditionNotMetException as e:
                pre_conditions_not_met.append(e.__str__())
        
        if pre_conditions_not_met:
            MESSAGE_ERROR = ", ".join(pre_conditions_not_met)
            raise PreConditionNotMetException(MESSAGE_ERROR)

    def _get_config(self):
        options = webdriver.ChromeOptions()

        download_path = self.default_download_path
        prefs = {
            "download.default_directory": str(download_path),
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
        }
        options.add_experimental_option("prefs", prefs)

        return options

    def _get_webdriver(self):
        options = self._get_config()
        webdriver_instance = webdriver.Chrome(options=options)
        return webdriver_instance
        

    