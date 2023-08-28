from dotenv import load_dotenv
import os

load_dotenv()

# DATABASE CONFIGURATION
SQLALCHEMY_DATABASE_URL =  os.getenv("SQLALCHEMY_DATABASE_URL")
