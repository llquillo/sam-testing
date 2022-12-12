from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from data.db import Database

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    cognito_username = Column(String)

if __name__ == "__main__":
    meta = MetaData()
    db = Database()
    meta.create_all(db._engine)
