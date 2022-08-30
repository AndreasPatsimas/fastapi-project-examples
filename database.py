from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# MYSQL Series
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mySql!9!4AP@127.0.0.1:3306/todoapp"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# MYSQL Series
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.flush()
            db.close()
