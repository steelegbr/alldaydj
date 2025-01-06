from pydantic import BaseModel


class AppSettings(BaseModel):
    auth_audience: str
    auth_domain: str
    auth_client_id: str
