from motor.motor_asyncio import AsyncIOMotorClient
from services.settings import get_settings

# Connection

settings = get_settings()
client = AsyncIOMotorClient(settings.mongodb_url)
db = client.alldaydj

# Collections

genre_collection = db.get_collection("genre")
tag_collection = db.get_collection("tag")
type_collection = db.get_collection("type")

# Indexes

genre_collection.create_index("genre", unique=True)
tag_collection.create_index("tag", unique=True)
type_collection.create_index("cart_type", unique=True)
