import os
import sqlalchemy
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set in .env file.")

# Test database connection
try:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 'Connection Successful'"))
        print("✅ Database Connected: ", result.fetchone()[0])
except Exception as e:
    print("❌ Database Connection Failed: ", str(e))
