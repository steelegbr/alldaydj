from pydantic import BaseModel, HttpUrl


class Settings(BaseModel):
    base_url: HttpUrl = HttpUrl("http://localhost:8000")
