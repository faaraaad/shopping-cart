import requests
from payment.models import Product
from django.contrib.auth.models import User

products = requests.get("https://fakestoreapi.com/products")
products_data = products.json()

for product in products_data:
    Product.objects.get_or_create(
        title=product.get("title"),
        price=product.get("price"),
        description=product.get("description"),
        category=product.get("category"),
        image=product.get("image"),
        rating=product.get("rating").get("rate"),
        raters=product.get("rating").get("count"),
    )

if not User.objects.filter(username="superuser").exists():
    User.objects.create_superuser("superuser", password="GreatPassword")
