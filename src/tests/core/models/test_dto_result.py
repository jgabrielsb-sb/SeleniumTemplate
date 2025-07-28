import pytest

from core.models.dto import dto_result
from core.models.enum import dto_status

class TestResult:
    def test_if_raises_error_when_status_is_failed_and_why_error_is_none(self):
        with pytest.raises(ValueError):
            dto_result.Result(
                status=dto_status.Status.FAILED,
                why_error=None
            )   


