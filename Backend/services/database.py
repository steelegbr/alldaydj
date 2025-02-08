from motor.motor_asyncio import AsyncIOMotorClient
from services.settings import get_settings

# Connection

settings = get_settings()
client = AsyncIOMotorClient(settings.mongodb_url)
db = client.alldaydj

# Collections

tag_collection = db.get_collection("tag")

# Indexes

tag_collection.create_index("tag", unique=True)
