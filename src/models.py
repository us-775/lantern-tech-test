from typing import Any, Literal

from pydantic import BaseModel, Field


class DataComparison(BaseModel):
    field: str = Field(..., validation_alias="key")
    action: Literal["no change", "deleted", "added", "updated"]
    old_value: Any
    new_value: Any
