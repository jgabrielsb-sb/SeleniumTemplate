from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from typing import List

from interfaces.selenium.base_action import BaseAction

from core.messages import *

from core.models.dto import dto_result
from core.models.enum import dto_status

class BaseComposedAction(ABC):
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
    def _get_actions(self) -> List[BaseAction]:
        pass

    def get_actions(self) -> List[BaseAction]:
        actions = self._get_actions()

        if not actions:
            raise ValueError(
                VARIABLE_CANNOT_BE_EMPTY.format(
                    variable_name='actions'
                    )
                )

        for action in actions:
            if not isinstance(action, BaseAction):
                raise ValueError(
                    ALL_ELEMENTS_OF_VARIABLE_MUST_BE_A_BASE_ACTION_INSTANCE.format(
                        variable_name='actions'
                        )
                    )
        
        return actions

    def run(self) -> dto_result.ComposedActionResult:
        actions = self.get_actions()

        actions_results = []

        for action in actions:
            action_result = action.run()
            actions_results.append(action_result)

        status = (
            dto_status.Status.SUCCESS
            if all(action_result.result.status == dto_status.Status.SUCCESS for action_result in actions_results)
            else dto_status.Status.FAILED
        )
        why_error = None

        if status == dto_status.Status.FAILED:
            why_error = SOME_ACTIONS_FAILED

        last_action_result = actions_results[-1].result.result

        return dto_result.ComposedActionResult(
            result=dto_result.Result(
                status=status,
                why_error=why_error,
                result=last_action_result
            ),
            report=actions_results
        )

