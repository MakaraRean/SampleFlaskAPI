
from database import Session
from app.models.models import Product

# 2 - extract a session
session = Session()

# 3 - extract all products
products = session.query(Product).all()

# 4 - print movies' details
print('\n### All products:')
for product in products:
    print(f'Product {product.id} has name {product.name} in category : {product.category.name}')
print('')