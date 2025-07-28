from core.exceptions.webdriver_exceptions import (
    InitiliazerException,
    PreConditionNotMetException
)

from infra.webdriver import SeleniumInitializer

import pytest

class TestBaseSeleniumInitializer:

    def test_if_raises_initializer_exception_when_pre_conditions_are_not_met(self):
        
        class InitializerWithPreConditionsNotMet(SeleniumInitializer):
            def _verify_pre_conditions(self):
                raise PreConditionNotMetException('test pre-condition not met')

            def _get_config(self):
                return 'TEST CONFIG'

            def _get_webdriver(self):
                return 'TEST WEBDRIVER'

        with pytest.raises(InitiliazerException):
            InitializerWithPreConditionsNotMet()

    def test_if_get_webdriver_raises_value_error_when_webdriver_is_not_a_webdriver_object(self):

        class InitializerWithWebdriverNotAWebdriverObject(SeleniumInitializer):
            def _verify_pre_conditions(self):
                return True

            def _get_config(self):
                return 'TEST CONFIG'

            def _get_webdriver(self):
                return 'NOT A WEBDRIVER OBJECT'

        with pytest.raises(ValueError):
            InitializerWithWebdriverNotAWebdriverObject().get_webdriver()
            
            
            