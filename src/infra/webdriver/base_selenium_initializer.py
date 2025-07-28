from abc import abstractmethod, ABC

from selenium.webdriver.chrome.webdriver import WebDriver

from core.exceptions.webdriver_exceptions import (
    PreConditionNotMetException,
    InitiliazerException
)


class SeleniumInitializer(ABC):
    def __init__(self):
        """
        Initializes a SeleniumInitializer.
        Arguments:
            selenium_config: a SeleniumConfig object
        Raises:
            PreConditionsNotMetException: if there is any conditions that will not allow 
            the proper use of the downloader.
        """
        self._verify_pre_conditions()

        
    @abstractmethod
    def _verify_pre_conditions(self):
        """
        For each Downloader, the inherited classes must implement this class. 
        The intention here is to provide an interface so as the webdriver itself 
        can verify if the environment met it's conditions to work properly.
        For example: for a certain downloader, you must verify if the default 
        download folder has sufficient permissions. 
        If a condition is not met, the inherited classes MUST:
            - raise PreConditionNotMetException.
        """
        pass

    def verify_pre_conditions(self):
        """
        Verifies if the pre-conditions are met.
        Raises:
            InitiliazerException: if the pre-conditions are not met.
        """
        try:
            self._verify_pre_conditions()
        except PreConditionNotMetException as e:
            raise InitiliazerException(e.__str__())

    @abstractmethod
    def _get_config(self):
        """
        The inherited classes must set it's own configurations.
        The inherited classes MUST:
            - set the webdriver configurations.
        """
        pass

    @abstractmethod
    def _get_webdriver(self):
        """
        Method that will compile the necessary steps and displays the webdriver.
        Should return a Selenium Webdriver Object.
        """
        pass

    def get_webdriver(self) -> WebDriver:
        """
        Returns a Selenium Webdriver Object.
        Raises:
            ValueError: if the webdriver object is not a Selenium.Webdriver object.
        """
        webdriver_object = self._get_webdriver()

        if not isinstance(webdriver_object, WebDriver):
            raise ValueError('webdriver should of type Selenium.Webdriver')

        return webdriver_object