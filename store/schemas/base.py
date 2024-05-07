from datetime import datetime
from decimal import Decimal

from bson import Decimal128
from pydantic import BaseModel, model_validator, UUID4, Field


class BaseSchemaMixin(BaseModel):
    class Config:
        from_attributes = True


class OutMixin(BaseModel):
    id: UUID4 = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @model_validator(mode="before")
    def set_schema(cls, data):
        for key, value in data.items():
            if isinstance(value, Decimal128):
                data[key] = Decimal(str(value))

        return data
