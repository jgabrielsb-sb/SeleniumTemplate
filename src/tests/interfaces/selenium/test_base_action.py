
from argparse import Action
import pytest

from unittest.mock import MagicMock

from selenium.webdriver.chrome.webdriver import WebDriver

from core.exceptions.selenium_exceptions import SeleniumBaseActionException

from core.models.dto.dto_result import Attempt
from interfaces.selenium import base_action

from core.messages import (
    VARIABLE_MUST_BE_A_WEBDRIVER_INSTANCE,
    VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0,
    ALL_ATTEMPTS_FAILED_MESSAGE
)

from core.models.enum import dto_status


class TestBaseAction:

    @pytest.fixture
    def mock_webdriver(self):
        return MagicMock(spec=WebDriver)

    @pytest.fixture
    def base_action_class(self):
        class BaseAction(base_action.BaseAction):
            def _execute_action(self):
                return 'success'
        
        return BaseAction

    def test_if_raises_error_when_webdriver_instance_is_not_a_webdriver_instance(
        self,
        base_action_class,
        mock_webdriver
    ):
        with pytest.raises(ValueError) as e:
            base_action_class(webdriver_instance='not_a_webdriver_instance', attempts=1)
        
        assert e.value.args[0] == VARIABLE_MUST_BE_A_WEBDRIVER_INSTANCE.format(variable_name='webdriver_instance')

    def test_if_raises_error_when_attempts_is_not_an_integer(
        self,
        base_action_class,
        mock_webdriver
    ):
        with pytest.raises(ValueError) as e:
            base_action_class(webdriver_instance=mock_webdriver, attempts='not_an_integer')

        assert e.value.args[0] == VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0.format(variable_name='attempts')

    def test_if_raises_error_when_attempts_is_less_than_1(
        self,
        base_action_class,
        mock_webdriver
    ):
        with pytest.raises(ValueError) as e:
            base_action_class(webdriver_instance=mock_webdriver, attempts=0)

        assert e.value.args[0] == VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0.format(variable_name='attempts')

    def test_run_failed_when_only_one_attempt_is_performed(
        self,
        base_action_class,
        mock_webdriver
    ):
        base_action_instance = base_action_class(webdriver_instance=mock_webdriver, attempts=1)
        
        def raise_error():
            raise SeleniumBaseActionException('test')
        
        base_action_instance._execute_action = raise_error
        
        action_result = base_action_instance.run()
        assert action_result.result.status == dto_status.Status.FAILED
        assert action_result.result.why_error == ALL_ATTEMPTS_FAILED_MESSAGE
        assert action_result.result.result == None
        
        # attempts assertion
        assert len(action_result.attempts) == 1
        first_attempt = action_result.attempts[0]
        assert first_attempt.attempt_index == 1
        assert first_attempt.why_error == 'test'

    def test_run_failed_when_more_than_one_attempt_is_performed(
        self,
        base_action_class,
        mock_webdriver
    ):
        base_action_instance = base_action_class(webdriver_instance=mock_webdriver, attempts=2)
        
        def raise_error():
            raise SeleniumBaseActionException('test')
        
        base_action_instance._execute_action = raise_error
        
        action_result = base_action_instance.run()
        assert action_result.result.status == dto_status.Status.FAILED
        assert action_result.result.why_error == ALL_ATTEMPTS_FAILED_MESSAGE
        assert action_result.result.result == None
        
        # attempts assertion
        assert len(action_result.attempts) == 2
        first_attempt = action_result.attempts[0]
        assert first_attempt.attempt_index == 1
        assert first_attempt.why_error == 'test'

        second_attempt = action_result.attempts[1]
        assert second_attempt.attempt_index == 2
        assert second_attempt.why_error == 'test'

    def test_run_sucess_when_failed_on_first_attempt_and_success_on_second_attempt(
        self,
        base_action_class,
        mock_webdriver
    ):
        attempts = 2
        base_action_instance = base_action_class(webdriver_instance=mock_webdriver, attempts=attempts)

        call_count = {'count': 0}

        def execute_action_with_retry():
            if call_count['count'] == 0:
                call_count['count'] += 1
                raise SeleniumBaseActionException('test')
            return 'success'

        base_action_instance._execute_action = execute_action_with_retry

        action_result = base_action_instance.run()
        assert action_result.result.status == dto_status.Status.SUCCESS
        assert action_result.result.result == 'success'
        
        # attempts assertion
        assert len(action_result.attempts) == 1
        first_attempt = action_result.attempts[0]
        assert first_attempt.attempt_index == 1
        assert first_attempt.why_error == 'test'



    def test_run_success_when_action_is_executed_successfully_on_first_attempt(
        self,
        base_action_class,
        mock_webdriver
    ):
        attempts = 3
        base_action_instance = base_action_class(webdriver_instance=mock_webdriver, attempts=attempts)

        action_result = base_action_instance.run()
        assert action_result.result.status == dto_status.Status.SUCCESS
        assert action_result.result.result == 'success'
        
        # attempts assertion
        assert len(action_result.attempts) == 0
        