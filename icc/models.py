from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from pydantic.json import ENCODERS_BY_TYPE


""" Model Groundwork """


class PydanticObjectId(ObjectId):
    """
    Object Id field. Compatible with Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return PydanticObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(
            type="string",
        )


ENCODERS_BY_TYPE[PydanticObjectId] = str


class IccBaseModel(BaseModel):
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


""" Request DTOs """


class LightingRequest(IccBaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    target: Optional[PydanticObjectId]
    name: Optional[str]
    operation: str
    h: int = 0
    s: int = 100
    v: int = 50
    brightness: int = None
    temperature: int = None
    date: datetime = datetime.utcnow().isoformat()


class PowerRequest(IccBaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    target: Optional[PydanticObjectId]
    name: Optional[str]
    operation: str


class SceneRequest(IccBaseModel):
    name: str
    date: datetime = datetime.utcnow().isoformat()


class ChromecastRequest(IccBaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    target: PydanticObjectId
    path: str


""" DTOs """


class CreateLightingRequestDto(IccBaseModel):
    target_id: str
    operation: str
    h: int = 0
    s: int = 100
    v: int = 50
    brightness: int = None
    temperature: int = None


class CreatePowerRequestDto(IccBaseModel):
    target_id: str
    operation: str


class CreateSceneDto(IccBaseModel):
    name: str
    lighting_requests: Optional[list[CreateLightingRequestDto]]
    power_requests: Optional[list[CreatePowerRequestDto]]


""" Entitity Models """


class Device(IccBaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    name: str
    type: str
    model: str
    ip: str


class State(IccBaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    device: PydanticObjectId
    state: bool
    date: datetime = datetime.utcnow()


class SceneModel(IccBaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias="_id")
    name: str
    lighting_requests: Optional[list[LightingRequest]]
    power_requests: Optional[list[PowerRequest]]


""" IoT Devices Global Strings """


class LightingDeviceTypes:
    KasaBulb: str = "Kasa Bulb"
    CustomLedStrip: str = "Custom Led Strip"
    KasaLedStrip: str = "Kasa Led Strip"


class PowerDeviceTypes:
    KasaPlug: str = "Kasa Plug"
