from app.database.connection import engine
from app.models.user import User
from app.database.connection import Base

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()