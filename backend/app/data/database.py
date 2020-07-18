from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.common.config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = Session()
