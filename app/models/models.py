
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    createAt = Column(DateTime)

    def __init__(self, name, createAt):
        self.name = name
        self.createAt = createAt


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    qty = Column(Integer)
    price = Column(Float)
    createdAt = Column(DateTime)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", backref="products")

    def __init__(self, name, qty, price, createdAt, category_id):
        self.name = name
        self.qty = qty
        self.price = price
        self.createdAt = createdAt
        self.category_id = category_id


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password
