import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variable
mongodb_uri = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(mongodb_uri)

# Reference to the MongoDB database
db = client["graph_db"]