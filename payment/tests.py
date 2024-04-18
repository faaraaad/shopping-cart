from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch, MagicMock

from django.urls import reverse

from payment.models import Product


class TestShoppingCartUseCases(TestCase):
    def setUp(self):
        products = [
            {
                "id": 1,
                "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
                "price": "109.95",
                "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
                "category": "men's clothing",
                "image": "http://localhost/https%3A/fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
                "rating": "3.90",
                "raters": 120
            },
            {
                "id": 2,
                "title": "Mens Casual Premium Slim Fit T-Shirts ",
                "price": "22.30",
                "description": "Slim-fitting style, contrast raglan long sleeve, three-button henley placket, light weight & soft fabric for breathable and comfortable wearing. And Solid stitched shirts with round neck made for durability and a great fit for casual fashion wear and diehard baseball fans. The Henley style round neckline includes a three-button placket.",
                "category": "men's clothing",
                "image": "http://localhost/https%3A/fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg",
                "rating": "4.10",
                "raters": 259
            },
            {
                "id": 3,
                "title": "Mens Cotton Jacket",
                "price": "55.99",
                "description": "great outerwear jackets for Spring/Autumn/Winter, suitable for many occasions, such as working, hiking, camping, mountain/rock climbing, cycling, traveling or other outdoors. Good gift choice for you or your family member. A warm hearted love to Father, husband or son in this thanksgiving or Christmas Day.",
                "category": "men's clothing",
                "image": "http://localhost/https%3A/fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg",
                "rating": "4.70",
                "raters": 500
            }]

        for product in products:
            Product.objects.create(
                title=product.get("title"),
                price=product.get("price"),
                description=product.get("description"),
                category=product.get("category"),
                image=product.get("image"),
                rating=product.get("rating"),
                raters=product.get("raters")
            )

        user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        user.is_active = True
        user.save()

    def test_empty_list_products(self):
        url_token = reverse("token-obtain")
        resp = self.client.post(url_token, data={
            "username": "user",
            "password": "pass"
        })
        access_token = resp.json().get("access")
        self.assertEqual(resp.status_code, 200)

        list_url = reverse("shopping-cart-list")
        list_shopping_cart = self.client.get(list_url,
                                             headers={f"Authorization": f"Bearer {access_token}"}
                                             ).json()
        self.assertEqual(len(list_shopping_cart), 0)

    def test_modify_list_products(self):
        """
        In this scenario first we add 10 number of a product to a user shopping cart
        after that we remove 5 of them
        finally, the quantity of the product in shopping cart should 5
        """
        url_token = reverse("token-obtain")
        resp = self.client.post(url_token, data={
            "username": "user",
            "password": "pass"
        })
        access_token = resp.json().get("access")

        product_id = Product.objects.first().id
        add_url = reverse("shopping-cart-add", kwargs={"product_id": product_id})
        for i in range(10):
            self.client.post(add_url,
                             headers={f"Authorization": f"Bearer {access_token}"},
                             )

        remove_url = reverse("shopping-cart-remove", kwargs={"product_id": product_id})
        for i in range(5):
            self.client.post(remove_url,
                             headers={f"Authorization": f"Bearer {access_token}"},
                             )

        list_url = reverse("shopping-cart-list")
        list_shopping_cart = self.client.get(list_url,
                                             headers={f"Authorization": f"Bearer {access_token}"}
                                             )

        self.assertEqual(list_shopping_cart.json()[0].get('quantity'), 5)
