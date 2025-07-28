from infra.webdriver.base_selenium_executor import SeleniumExecutor
from infra.selenium import selenium_process

class DefaultExecutor(SeleniumExecutor):
    """
    Default executor for selenium processes.
    This executor is used to execute selenium processes.
    """
    def _execute(self, selenium_process: selenium_process.SeleniumProcess) -> object:
        return selenium_process.execute()