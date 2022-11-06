from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


class LightingRequest(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    target: str
    operation: str
    date: datetime = datetime.utcnow().isoformat()

    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


class HsvRequest(LightingRequest):
    brightness: Optional[int]
    h: int = 0
    s: int = 100
    v: int = 50


class BrightnessRequest(LightingRequest):
    brightness: int


class TemperatureRequest(LightingRequest):
    brightness: Optional[int]
    temperature: str
