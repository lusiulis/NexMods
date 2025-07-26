import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "backend" / "products" / ".env.local")

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")