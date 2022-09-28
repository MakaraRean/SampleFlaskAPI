from models import Category, User, Product
from database import Base,engine,Session
from datetime import datetime


# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()


# 4 - create product
session.add(User("",""))