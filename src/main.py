from infra.webdriver import webdriver_instance

if __name__ == '__main__':
    webdriver_instance.get('https://www.google.com')
    print(webdriver_instance.title)