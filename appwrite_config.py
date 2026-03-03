import os
from dotenv import load_dotenv
from appwrite.client import Client
from appwrite.services.databases import Databases

load_dotenv()

# Replace with your real values
APPWRITE_ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
API_KEY = os.getenv("APPWRITE_API_KEY")

DATABASE_ID = os.getenv("APPWRITE_DATABASE_ID")
USERS_COLLECTION_ID = os.getenv("APPWRITE_USERS_COLLECTION")
CONTACTS_COLLECTION_ID = os.getenv("APPWRITE_CONTACTS_COLLECTION")

# print("Endpoint:", os.getenv("APPWRITE_ENDPOINT"))
# print("Project:", os.getenv("APPWRITE_PROJECT_ID"))
# print("API Key:", os.getenv("APPWRITE_API_KEY"))
# print("Database:", os.getenv("APPWRITE_DATABASE_ID"))


def get_databases():
    client = Client()
    client.set_endpoint(APPWRITE_ENDPOINT)
    client.set_project(PROJECT_ID)
    client.set_key(API_KEY)
    
    return Databases(client)