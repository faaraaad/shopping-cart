import os
import requests
from payment.models import Product
from django.contrib.auth.models import User

# Try to fetch products from Fakestore API, with a local fallback if offline or down
try:
    print("Fetching products from fakestoreapi.com...")
    response = requests.get("https://fakestoreapi.com/products", timeout=10)
    response.raise_for_status()
    products_data = response.json()
    print(f"Successfully fetched {len(products_data)} products.")
except Exception as e:
    print(f"Error fetching from API: {e}. Using offline fallback products instead.")
    products_data = [
        {
            "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
            "price": 109.95,
            "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
            "category": "men's clothing",
            "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
            "rating": {"rate": 3.9, "count": 120}
        },
        {
            "title": "Mens Casual Premium Slim Fit T-Shirts",
            "price": 22.30,
            "description": "Slim-fitting style, contrast raglan long sleeve, three-button henley placket, light weight & soft fabric for breathable and comfortable wearing.",
            "category": "men's clothing",
            "image": "https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg",
            "rating": {"rate": 4.1, "count": 259}
        },
        {
            "title": "Mens Cotton Jacket",
            "price": 55.99,
            "description": "great outerwear jackets for Spring/Autumn/Winter, suitable for many occasions, such as working, hiking, camping, mountain/rock climbing.",
            "category": "men's clothing",
            "image": "https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg",
            "rating": {"rate": 4.7, "count": 500}
        },
        {
            "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
            "price": 695.0,
            "description": "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl.",
            "category": "jewelry",
            "image": "https://fakestoreapi.com/img/71pWzhdJNwL._AC_UL640_.jpg",
            "rating": {"rate": 4.6, "count": 400}
        },
        {
            "title": "Solid Gold Petite Micropave",
            "price": 168.0,
            "description": "Satisfaction Guaranteed. Return or exchange any order within 30 days. Designed and sold by Hafeez Center in the United States.",
            "category": "jewelry",
            "image": "https://fakestoreapi.com/img/61sbMiUnoGL._AC_UL640_.jpg",
            "rating": {"rate": 3.9, "count": 70}
        }
    ]

for product in products_data:
    rating_data = product.get("rating", {})
    rate = rating_data.get("rate") if isinstance(rating_data, dict) else rating_data
    count = rating_data.get("count") if isinstance(rating_data, dict) else 0

    Product.objects.get_or_create(
        title=product.get("title"),
        price=product.get("price"),
        description=product.get("description"),
        category=product.get("category"),
        image=product.get("image"),
        rating=rate,
        raters=count,
    )

superuser_username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "superuser")
superuser_password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "GreatPassword")

if not User.objects.filter(username=superuser_username).exists():
    from django.conf import settings
    # Warn if default credentials are used in a production environment
    if not settings.DEBUG and (superuser_username == "superuser" or superuser_password == "GreatPassword"):
        print("WARNING: Creating superuser with default credentials ('superuser' / 'GreatPassword') in production! "
              "Please override DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD env vars for safety.")
    
    User.objects.create_superuser(superuser_username, password=superuser_password)
    print(f"Created superuser '{superuser_username}' successfully.")
