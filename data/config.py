from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import environ

load_dotenv()

BOT_TOKEN = environ.get("BOT_TOKEN")  # Bot toekn
ADMINS = environ.get("ADMINS")  # adminlar ro'yxati
IP = environ.get("IP")  # Xosting ip manzili

engine = create_engine(environ.get("DATABASE_URL"))
Base = declarative_base()
