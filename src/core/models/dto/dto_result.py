from typing import (
    Optional, 
    Any,
    List
)

from pydantic import (
    BaseModel, 
    model_validator
)

from core.models.enum import dto_status

class Result(BaseModel):
    status: dto_status.Status
    why_error: Optional[str] = None
    result: Optional[Any] = None

    @model_validator(mode='after')
    def validate_why_error(self):
        if self.status == dto_status.Status.FAILED:
            if self.why_error is None:
                raise ValueError('why_error is required when status is FAILED')
        return self

class Attempt(BaseModel):
    attempt_index: int
    why_error: Optional[str] = None

class ActionResult(BaseModel):
    result: Result
    attempts: Optional[List[Attempt]] = None

class ComposedActionResult(BaseModel):
    result: Result
    report: List[ActionResult]

   