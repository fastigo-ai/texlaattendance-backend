from pymongo import MongoClient
import os

MONGO_URL = "mongodb+srv://fastigoltd_db_user:S6GGfxgbrXqtH6G4@cluster0.ks1w4np.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["test"]

users_collection = db["users"]
visits_collection = db["visits"]
end_day_collection = db["end_day_photos"]
leave_collection = db["leave_requests"]