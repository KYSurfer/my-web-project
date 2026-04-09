import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_PATH = 'database.db'
    TOKEN_EXPIRY_HOURS = 48