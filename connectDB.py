from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="postgresql",
    username="postgres",
    host="localhost",
    database="fast",
    password="postgres",
)

engine = create_engine(url, echo=False)
connection = engine.connect()
session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
