from sqlalchemy import create_engine, text
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_database_url():
    # Try to read from .env file directly if available
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.strip().startswith("DATABASE_URL"):
                    url = line.split("=", 1)[1].strip().strip('"').strip("'")
                    return url
    
    # Fallback to config import
    try:
        from app.core.config import settings
        return settings.DATABASE_URL
    except Exception as e:
        print(f"Could not load config: {e}")
        return None

def upgrade():
    db_url = get_database_url()
    if not db_url:
        print("Error: DATABASE_URL not found.")
        return

    print(f"Connecting to database...")
    # Handle postgres connection string fix if needed
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(db_url)
    with engine.connect() as connection:
        try:
            # Check if column exists
            # For PostgreSQL, we query information_schema
            result = connection.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name='companies' AND column_name='logo_url'"
            ))
            exists = result.fetchone()
            
            if not exists:
                print("Adding logo_url column to companies table...")
                connection.execute(text("ALTER TABLE companies ADD COLUMN logo_url VARCHAR(500)"))
                connection.commit()
                print("Column added successfully.")
            else:
                print("Column logo_url already exists.")
                
        except Exception as e:
            print(f"Error executing migration: {e}")

if __name__ == "__main__":
    upgrade()
