from sqlalchemy import text
from app.db.database import engine, SessionLocal

def seed():
    with engine.connect() as conn:
        try:
            # Create a test employer user if not exists
            conn.execute(text("INSERT INTO users (full_name, email, password, role, status) VALUES ('Global Employer', 'employer@origin.com', 'password123', 'employer', 'approved') ON CONFLICT (email) DO NOTHING"))
            
            # Get the user id (assuming 1 for simplicity or searching)
            res = conn.execute(text("SELECT id FROM users WHERE email = 'employer@origin.com'")).fetchone()
            if not res:
                print("Failed to ensure employer user.")
                return
            user_id = res[0]

            # Create Companies
            companies = [
                ('TechCorp Solutions', 'info@techcorp.com', 'Bangalore, India', 'Leading software solutions.', user_id),
                ('Innovation Labs', 'hr@innovation.io', 'Remote', 'Experimental tech research.', user_id)
            ]
            for c in companies:
                conn.execute(text("INSERT INTO companies (company_name, email, location, description, user_id) VALUES (:name, :email, :loc, :desc, :uid) ON CONFLICT (email) DO NOTHING"), 
                             {"name": c[0], "email": c[1], "loc": c[2], "desc": c[3], "uid": c[4]})

            # Refresh to get IDs
            res = conn.execute(text("SELECT id FROM companies WHERE email = 'info@techcorp.com'")).fetchone()
            tc_id = res[0] if res else None
            
            res = conn.execute(text("SELECT id FROM companies WHERE email = 'hr@innovation.io'")).fetchone()
            il_id = res[0] if res else None

            if tc_id:
                conn.execute(text("INSERT INTO jobs (title, company_id, location, salary, skills_required, description, status) VALUES ('Senior Developer', :cid, 'Bangalore', '15-25 LPA', 'React, Python', 'Main developer role', 'approved')"), {"cid": tc_id})
                conn.execute(text("INSERT INTO part_time_jobs (title, company_id, location, salary, skills, description) VALUES ('Content Helper', :cid, 'Remote', '10,000/mo', 'SEO, Writing', 'Assist with blog posts')"), {"cid": tc_id})

            if il_id:
                conn.execute(text("INSERT INTO jobs (title, company_id, location, salary, skills_required, description, status) VALUES ('Research Engineer', :cid, 'Remote', '20-30 LPA', 'AI, ML', 'Research into future tech', 'approved')"), {"cid": il_id})
                conn.execute(text("INSERT INTO part_time_jobs (title, company_id, location, salary, skills, description) VALUES ('Data Labeler', :cid, 'Remote', '15,000/mo', 'ML, Focus', 'Label data for AI training')"), {"cid": il_id})

            conn.commit()
            print("Database seeded successfully via raw SQL!")
        except Exception as e:
            conn.rollback()
            print(f"Error seeding: {e}")

if __name__ == "__main__":
    seed()
