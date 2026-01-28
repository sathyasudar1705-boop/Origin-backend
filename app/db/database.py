from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from app.core.config import settings

# Handle potential postgres:// prefix from Supabase/Heroku
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)
SessionLocal = sessionmaker (bind=engine,autoflush=False,autocommit=False)


Base = declarative_base()
