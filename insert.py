from app.models.models import Category, Product
from database import Base,engine,Session
from datetime import datetime


# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()


# 4 - create product
beer = Category(name="Beer",createAt=datetime.now())
energy = Category(name="Energy Drink",createAt=datetime.now())


# 5 - create product
cambodia = Product(name= "Cambodia Beer",qty=5, price= 2000, createAt= datetime.now(), category= beer)
angkor = Product(name= "Angkor Beer",qty=5, price= 2000, createAt= datetime.now(), category=beer)
tiger = Product(name= "Tiger Beer",qty=5, price= 2000, createAt= datetime.now(), category=beer)

# 6 - persists data
session.add(beer)
session.add(energy)

session.add(cambodia)
session.add(angkor)
session.add(tiger)

# 7 - commit and close session
session.commit()
session.close()