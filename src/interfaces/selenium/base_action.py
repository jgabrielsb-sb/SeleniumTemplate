from typing import Any

from selenium.webdriver.chrome.webdriver import WebDriver

from abc import ABC, abstractmethod

from core.exceptions.selenium_exceptions import SeleniumBaseActionException

from core.models.dto import dto_result 
from core.models.enum import dto_status

from core.messages import (
    ALL_ATTEMPTS_FAILED_MESSAGE,
    VARIABLE_MUST_BE_A_WEBDRIVER_INSTANCE,
    VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0
)

class BaseAction(ABC):
    def __init__(self, webdriver_instance: WebDriver, attempts: int = 1):
        if not isinstance(webdriver_instance, WebDriver):
            raise ValueError(
                VARIABLE_MUST_BE_A_WEBDRIVER_INSTANCE.format(
                    variable_name='webdriver_instance'
                    )
                )
        
        if not isinstance(attempts, int) or attempts < 1:
            raise ValueError(
                VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0.format(
                    variable_name='attempts'
                    )
                )

        self.attempts = attempts
        self.webdriver_instance = webdriver_instance

    @abstractmethod
    def _execute_action(self) -> Any:
        pass

    def run(self) -> dto_result.Result:
        retries = []

        status = dto_status.Status.FAILED
        why_error = None
        result = None

        atempt_index = 1

        while atempt_index <= self.attempts:
            try:
                result = self._execute_action()
                status = dto_status.Status.SUCCESS
                break
            except SeleniumBaseActionException as e:
                why_error_on_attempt = str(e)
                
                attempt = dto_result.Attempt(
                    attempt_index=atempt_index,
                    why_error=why_error_on_attempt
                )

                retries.append(attempt)
                atempt_index += 1

        if status == dto_status.Status.FAILED:
            why_error = ALL_ATTEMPTS_FAILED_MESSAGE

        result = dto_result.Result(
            status=status,
            why_error=why_error,
            result=result
        )

        return dto_result.ActionResult(
            result=result,
            attempts=retries
        )
            


        
            



        
            
        
        
