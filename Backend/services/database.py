from motor.motor_asyncio import AsyncIOMotorClient
from services.settings import get_settings

settings = get_settings()
client = AsyncIOMotorClient(settings.mongodb_url)
db = client.alldaydj

tag_collection = db.get_collection("tag")
