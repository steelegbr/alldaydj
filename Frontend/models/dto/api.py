from pydantic import BaseModel


class ApiSettings(BaseModel):
    auth_audience: str
    auth_domain: str
    auth_client_id: str
