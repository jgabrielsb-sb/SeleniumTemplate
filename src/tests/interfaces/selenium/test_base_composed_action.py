
import pytest

from unittest.mock import MagicMock

from selenium.webdriver.remote.webdriver import WebDriver

from interfaces.selenium import (
    BaseAction,
    BaseComposedAction
)
from unittest.mock import create_autospec

from core.exceptions import SeleniumBaseActionException

from core.models.enum import dto_status

from core.messages import *

class TestBaseComposedAction:

    @pytest.fixture
    def mock_webdriver(self):
        return create_autospec(WebDriver, instance=True)


    @pytest.fixture
    def base_action_sucess(self):

        class SuccessAction(BaseAction):
            def _execute_action(self):
                return 'success'

        return SuccessAction

    @pytest.fixture
    def base_action_failed(self):
        class FailedAction(BaseAction):
            def _execute_action(self):
                raise SeleniumBaseActionException('failed')

        return FailedAction

    @pytest.fixture
    def base_composed_action_with_just_success_action(
        self,
        base_action_sucess
    ):
        class JustSuccessComposedAction(BaseComposedAction):
            def _get_actions(self):
                return [
                    base_action_sucess(
                        webdriver_instance=self.webdriver_instance,
                        attempts=1
                    )
                ]
        return JustSuccessComposedAction

    @pytest.fixture
    def base_composed_action_with_just_failed_action(
        self,
        base_action_failed
    ):
        class JustFailedComposedAction(BaseComposedAction):
            def _get_actions(self):
                return [
                    base_action_failed(
                        webdriver_instance=self.webdriver_instance,
                        attempts=1
                    )
                ]
        return JustFailedComposedAction

    @pytest.fixture
    def base_composed_action_with_success_and_failed_action(
        self,
        base_action_sucess,
        base_action_failed
    ):
        class SuccessAndFailedComposedAction(BaseComposedAction):
            def _get_actions(self):
                return [
                    base_action_sucess(
                        webdriver_instance=self.webdriver_instance,
                        attempts=1
                    ),
                    base_action_failed(
                        webdriver_instance=self.webdriver_instance,
                        attempts=1
                    )
                ]
        return SuccessAndFailedComposedAction
    
    def test_if_raises_value_error_if_webdriver_instance_is_not_a_webdriver_instance(
        self,
        base_composed_action_with_just_success_action
    ):
        with pytest.raises(ValueError) as e:
            base_composed_action_with_just_success_action(
                webdriver_instance='not_a_webdriver_instance',
                attempts=1
            )
        assert str(e.value) == VARIABLE_MUST_BE_A_WEBDRIVER_INSTANCE.format(
            variable_name='webdriver_instance'
        )

    def test_if_raises_value_error_if_attempts_is_not_an_integer_greater_than_0(
        self,
        base_composed_action_with_just_success_action,
        mock_webdriver
    ):
        with pytest.raises(ValueError) as e:
            base_composed_action_with_just_success_action(
                webdriver_instance=mock_webdriver,
                attempts=-2
            )

        assert str(e.value) == VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0.format(
            variable_name='attempts'
        )

    def test_if_get_actions_raises_value_error_if_actions_is_empty(
        self,
        mock_webdriver
    ):
        class EmptyComposedAction(BaseComposedAction):
            def _get_actions(self):
                return []

        with pytest.raises(ValueError) as e:
            EmptyComposedAction(
                webdriver_instance=mock_webdriver,
                attempts=1
            ).get_actions()

        assert str(e.value) == VARIABLE_CANNOT_BE_EMPTY.format(
            variable_name='actions'
        )

    def test_if_get_actions_raises_value_error_if_not_all_actions_are_base_action_instances(
        self,
        base_composed_action_with_just_success_action,
        mock_webdriver
    ):
        class NotAllActionsAreBaseActionInstances(BaseComposedAction):
            def _get_actions(self):
                return [
                    base_composed_action_with_just_success_action(
                        webdriver_instance=mock_webdriver,
                        attempts=1
                    ),
                    'not_a_base_action_instance'
                ]
        
        with pytest.raises(ValueError) as e:
            NotAllActionsAreBaseActionInstances(
                webdriver_instance=mock_webdriver,
                attempts=1
            ).get_actions()
        
        assert str(e.value) == ALL_ELEMENTS_OF_VARIABLE_MUST_BE_A_BASE_ACTION_INSTANCE.format(
            variable_name='actions'
        )

    def test_if_run_returns_success_when_all_actions_are_success(
        self,
        base_composed_action_with_just_success_action,
        mock_webdriver
    ):
        composed_action = base_composed_action_with_just_success_action(
            webdriver_instance=mock_webdriver,
            attempts=1
        )

        composed_action_result = composed_action.run()

        assert composed_action_result.result.status == dto_status.Status.SUCCESS
        assert len(composed_action_result.report) == 1
        assert composed_action_result.report[0].result.status == dto_status.Status.SUCCESS
        assert composed_action_result.report[0].result.result == 'success'
        assert composed_action_result.report[0].result.why_error is None

    def test_if_run_returns_failed_when_all_actions_are_failed(
        self,
        base_composed_action_with_just_failed_action,
        mock_webdriver
    ):
        composed_action = base_composed_action_with_just_failed_action(
            webdriver_instance=mock_webdriver,
            attempts=1
        )

        composed_action_result = composed_action.run()

        # result asserts
        assert composed_action_result.result.status == dto_status.Status.FAILED
        assert composed_action_result.result.result is None
        assert composed_action_result.result.why_error == SOME_ACTIONS_FAILED

        # report asserts
        assert len(composed_action_result.report) == 1
        assert composed_action_result.report[0].result.status == dto_status.Status.FAILED
        assert composed_action_result.report[0].result.result is None
        assert composed_action_result.report[0].result.why_error == ALL_ATTEMPTS_FAILED_MESSAGE
        
        # assert attempts
        assert len(composed_action_result.report[0].attempts) == 1
        assert composed_action_result.report[0].attempts[0].attempt_index == 1
        assert composed_action_result.report[0].attempts[0].why_error == 'failed'
    
    def test_if_run_returns_failed_when_some_actions_are_failed(
        self,
        base_composed_action_with_success_and_failed_action,
        mock_webdriver
    ):
        composed_action = base_composed_action_with_success_and_failed_action(
            webdriver_instance=mock_webdriver,
            attempts=1
        )

        composed_action_result = composed_action.run()

        # result asserts
        assert composed_action_result.result.status == dto_status.Status.FAILED
        assert composed_action_result.result.result is None
        assert composed_action_result.result.why_error == SOME_ACTIONS_FAILED

        # report asserts
        assert len(composed_action_result.report) == 2

        # success action report asserts
        assert composed_action_result.report[0].result.status == dto_status.Status.SUCCESS
        assert composed_action_result.report[0].result.result == 'success'
        assert composed_action_result.report[0].result.why_error is None

        # failed action report asserts
        assert composed_action_result.report[1].result.status == dto_status.Status.FAILED
        assert composed_action_result.report[1].result.result is None
        assert composed_action_result.report[1].result.why_error == ALL_ATTEMPTS_FAILED_MESSAGE
        
        # success action attempts asserts
        assert composed_action_result.report[0].result.status == dto_status.Status.SUCCESS
        assert len(composed_action_result.report[0].attempts) == 0
        assert composed_action_result.report[0].result.result == 'success'
        assert composed_action_result.report[0].result.why_error is None

        # failed action attempts asserts
        assert composed_action_result.report[1].result.status == dto_status.Status.FAILED
        assert len(composed_action_result.report[1].attempts) == 1
        assert composed_action_result.report[1].attempts[0].attempt_index == 1
        assert composed_action_result.report[1].attempts[0].why_error == 'failed'

