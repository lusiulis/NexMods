import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / "backend" / "products" / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")

assert DATABASE_URL is not None, "DATABASE_URL no se cargó correctamente"