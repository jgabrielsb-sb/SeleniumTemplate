
#### Initializers ####

To create a new webdriver with your own specifications you can use the interface ```SeleniumInitializer```defined on the file```src/infra/webdriver/initializers/local_chrome_with_download_initializer.py```

You can then implement that interface by defining the necessary abstract methods.

#### How to turn the webdriver available as an option ####

After implementing the initializer you can make it available by editing the file ```src/infra/webdriver/webdriver.py```:

1. Extend the variable ```SUPPORTED_CONFIGS``` by settings the config variables that must be met to choose that webdriver type;

```python
SUPPORTED_CONFIGS = {
    'local_chrome_with_download':{
        'on_docker': False,
        'will_perform_downloads': True,
        'mode': 'local',
    }
    # EXTEND/EDIT to include your new webdriver type
}
```

2. Extend the function ```return_webdriver_instance``` to return the webdriver instance of your choice:

```python
def return_webdriver_instance(
    webdriver_config: dto_webdriver_config.WebdriverConfig
):
    webdriver_name = get_webdriver_name(webdriver_config)

    if webdriver_name == 'local_chrome_with_download':
        return LocalChromeWithDownloadInitializer(default_download_path=webdriver_config.default_download_path).get_webdriver()
    # elif ... EDIT to include your new webdriver type
    
    raise ValueError(f"No matching supported webdriver config found for: {webdriver_name}")

```

