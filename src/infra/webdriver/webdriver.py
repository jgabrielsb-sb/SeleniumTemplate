from config import webdriver_config

from core.models import dto_webdriver_config

from infra.webdriver.initializers import LocalChromeWithDownloadInitializer

from pathlib import Path

SUPPORTED_CONFIGS = {
    'local_chrome_with_download':{
        'on_docker': False,
        'will_perform_downloads': True,
        'mode': 'local',
    }
}

def get_webdriver_name(webdriver_config: dto_webdriver_config.WebdriverConfig):
    for name, config in SUPPORTED_CONFIGS.items():
        if (
            config['on_docker'] == webdriver_config.on_docker and
            config['will_perform_downloads'] == webdriver_config.will_perform_downloads and
            config['mode'] == webdriver_config.mode
        ):
            return name
    raise ValueError(f"No matching supported webdriver config found for: {webdriver_config}")

def return_webdriver_instance(
    webdriver_config: dto_webdriver_config.WebdriverConfig
):
    webdriver_name = get_webdriver_name(webdriver_config)

    if webdriver_name == 'local_chrome_with_download':
        return LocalChromeWithDownloadInitializer(default_download_path=webdriver_config.default_download_path).get_webdriver()
    
    raise ValueError(f"No matching supported webdriver config found for: {webdriver_name}")

webdriver_instance = return_webdriver_instance(webdriver_config)
webdriver_instance.get('https://www.google.com')



