# generated by datamodel-codegen:
#   filename:  http://localhost:8002/openapi.json
#   timestamp: 2021-08-29T16:39:39+00:00

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: int = Field(..., title='Id')
    text: Dict[str, Any] = Field(..., title='Text')


class Status(BaseModel):
    message: str = Field(..., title='Message')


class ValidationError(BaseModel):
    loc: List[str] = Field(..., title='Location')
    msg: str = Field(..., title='Message')
    type: str = Field(..., title='Error Type')


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title='Detail')
