from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Modelos import Base

engine = create_engine("postgresql+psycopg:///productos")
Session = sessionmaker(engine)

Base.metadata.create_all(engine)