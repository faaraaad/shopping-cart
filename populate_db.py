import requests
from payment.models import Product

products = requests.get("https://fakestoreapi.com/products")
products_data = products.json()

for product in products_data:
    Product.objects.create(
        title=product.get("title"),
        price=product.get("price"),
        description=product.get("description"),
        category=product.get("category"),
        image=product.get("image"),
        rating=product.get("rating").get("rate"),
        raters=product.get("rating").get("count"),
    )
