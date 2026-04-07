from pydantic import BaseModel, HttpUrl, ConfigDict


class LinkRequest(BaseModel):
    original_url: HttpUrl


class LinkResponse(BaseModel):
    short_id: str

    model_config = ConfigDict(from_attributes=True)
