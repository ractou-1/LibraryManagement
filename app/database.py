from sqlalchemy import create_engine, text 
from sqlalchemy.orm import sessionmaker 
 
DATABASE_URL = "sqlite:///library.db" 
 
engine = create_engine( 
    DATABASE_URL, 
    connect_args={"check_same_thread": False} 
) 
 
SessionLocal = sessionmaker( 
    bind=engine, 
    autoflush=False, 
    autocommit=False 
) 
 
 
def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 

if __name__ == "__main__": 
    with engine.connect() as connection: 
        result = connection.execute(text("SELECT 3")) 
        print(result.scalar()) 