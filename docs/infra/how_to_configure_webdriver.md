#### The Purpose ####

The purpose of this template is to offer an interface where you can easily change the mode of the webdriver and then acess it on the project.

#### How to Configure your Webdriver Instance ####
The file where you can define the settings of your webdriver is ```src/config/wedriver_config.py```:

You can them define the specified variables by consulting the ```WebdriverConfig``` dto object.

For more details about the webdriver config, check the model defined on the file ```core/models/dto_webdriver_config```

#### How to acess the webdriver instance ####

By importing the ```webdriver_config``` file, the file ```src/infra/webdriver/webdriver.py``` will provide the webdriver instance for your configurations specifications.

You can them get it by exporting the ```webdriver_instance```. Example:

```python
from infra.webdriver import webdriver_instance

if __name__ == '__main__':
    webdriver_instance.get('https://www.google.com')
    print(webdriver_instance.title)
```






