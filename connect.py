import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

url_to_db = os.getenv("DATABASE_URL")

if not url_to_db:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
