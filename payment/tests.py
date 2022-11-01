from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from payment.models import Product, CartItem, ShoppingCart


class TestShoppingCartUseCases(TestCase):
    def setUp(self):
        # Create three test products
        self.p1 = Product.objects.create(
            title="Product 1",
            price="10.00",
            description="Description 1",
            category="category1",
            rating="4.00",
            raters=10,
        )
        self.p2 = Product.objects.create(
            title="Product 2",
            price="20.00",
            description="Description 2",
            category="category1",
            rating="4.50",
            raters=20,
        )
        self.p3 = Product.objects.create(
            title="Product 3",
            price="30.00",
            description="Description 3",
            category="category2",
            rating="5.00",
            raters=30,
        )

        # Create active test users
        self.user = User.objects.create_user(
            username="user", email="user@foo.com", password="pass"
        )
        self.user.is_active = True
        self.user.save()

        self.other_user = User.objects.create_user(
            username="other_user", email="other@foo.com", password="pass"
        )
        self.other_user.is_active = True
        self.other_user.save()

    def get_access_token(self, username, password):
        url_token = reverse("token-obtain")
        resp = self.client.post(
            url_token, data={"username": username, "password": password}
        )
        self.assertEqual(resp.status_code, 200)
        return resp.json().get("access")

    def test_empty_list_products(self):
        """
        An empty shopping cart should return an empty list.
        """
        list_url = reverse("shopping-cart-list")
        access_token = self.get_access_token("user", "pass")
        resp = self.client.get(
            list_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertEqual(len(resp.json()), 0)

    def test_modify_list_products(self):
        """
        Adding and removing items should correctly update quantities.
        """
        access_token = self.get_access_token("user", "pass")
        product_id = self.p1.id

        add_url = reverse("shopping-cart-add", kwargs={"product_id": product_id})
        for i in range(10):
            resp = self.client.post(
                add_url,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            self.assertEqual(resp.status_code, HTTP_201_CREATED)

        remove_url = reverse("shopping-cart-remove", kwargs={"product_id": product_id})
        for i in range(5):
            resp = self.client.post(
                remove_url,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            self.assertEqual(resp.status_code, HTTP_200_OK)

        list_url = reverse("shopping-cart-list")
        list_shopping_cart = self.client.get(
            list_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(list_shopping_cart.json()[0].get("quantity"), 5)

    def test_error_for_remove_empty_shopping_cart(self):
        """
        If shopping cart doesn't have a product, removing it should return NO_CONTENT.
        """
        access_token = self.get_access_token("user", "pass")
        product_id = self.p1.id

        remove_url = reverse("shopping-cart-remove", kwargs={"product_id": product_id})
        resp = self.client.post(
            remove_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)

    def test_add_non_existent_product(self):
        """
        Adding a product that does not exist in the database should return 404.
        """
        access_token = self.get_access_token("user", "pass")
        invalid_id = 99999
        add_url = reverse("shopping-cart-add", kwargs={"product_id": invalid_id})
        resp = self.client.post(
            add_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_remove_non_existent_product(self):
        """
        Removing a product that does not exist in the database should return 404.
        """
        access_token = self.get_access_token("user", "pass")
        invalid_id = 99999
        remove_url = reverse("shopping-cart-remove", kwargs={"product_id": invalid_id})
        resp = self.client.post(
            remove_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_unauthorized_access(self):
        """
        Accessing any shopping cart endpoint without authentication should return 401.
        """
        # List
        resp = self.client.get(reverse("shopping-cart-list"))
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

        # Add
        add_url = reverse("shopping-cart-add", kwargs={"product_id": self.p1.id})
        resp = self.client.post(add_url)
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

        # Remove
        remove_url = reverse("shopping-cart-remove", kwargs={"product_id": self.p1.id})
        resp = self.client.post(remove_url)
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)

    def test_add_response_contains_correct_quantities(self):
        """
        The POST add action response should contain the correct up-to-date quantity immediately.
        """
        access_token = self.get_access_token("user", "pass")
        add_url = reverse("shopping-cart-add", kwargs={"product_id": self.p1.id})

        # Add first time (quantity should be 1)
        resp1 = self.client.post(
            add_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(resp1.status_code, HTTP_201_CREATED)
        data1 = resp1.json()
        self.assertEqual(len(data1), 1)
        self.assertEqual(data1[0]["product"]["id"], self.p1.id)
        self.assertEqual(data1[0]["quantity"], 1)

        # Add second time (quantity should be 2 in the direct response)
        resp2 = self.client.post(
            add_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(resp2.status_code, HTTP_201_CREATED)
        data2 = resp2.json()
        self.assertEqual(len(data2), 1)
        self.assertEqual(data2[0]["product"]["id"], self.p1.id)
        self.assertEqual(data2[0]["quantity"], 2)

    def test_remove_to_zero_deletes_item(self):
        """
        Removing an item when its quantity is 1 should delete the CartItem completely.
        """
        access_token = self.get_access_token("user", "pass")
        add_url = reverse("shopping-cart-add", kwargs={"product_id": self.p1.id})
        remove_url = reverse("shopping-cart-remove", kwargs={"product_id": self.p1.id})

        # Add item
        self.client.post(add_url, headers={"Authorization": f"Bearer {access_token}"})

        # Remove item (quantity becomes 0, so should be deleted)
        resp = self.client.post(
            remove_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(resp.status_code, HTTP_200_OK)
        # The returned list of cart items should now be empty
        self.assertEqual(len(resp.json()), 0)

    def test_multi_user_isolation(self):
        """
        A user's shopping cart actions must not affect other users' carts.
        """
        token1 = self.get_access_token("user", "pass")
        token2 = self.get_access_token("other_user", "pass")

        add_url = reverse("shopping-cart-add", kwargs={"product_id": self.p1.id})

        # User 1 adds product 1
        self.client.post(add_url, headers={"Authorization": f"Bearer {token1}"})

        # User 2 lists cart (should be empty)
        resp2 = self.client.get(
            reverse("shopping-cart-list"),
            headers={"Authorization": f"Bearer {token2}"},
        )
        self.assertEqual(len(resp2.json()), 0)

        # User 2 adds product 1 twice
        self.client.post(add_url, headers={"Authorization": f"Bearer {token2}"})
        self.client.post(add_url, headers={"Authorization": f"Bearer {token2}"})

        # Check User 1 cart quantity (should still be 1)
        resp1 = self.client.get(
            reverse("shopping-cart-list"),
            headers={"Authorization": f"Bearer {token1}"},
        )
        self.assertEqual(resp1.json()[0]["quantity"], 1)

        # Check User 2 cart quantity (should be 2)
        resp2_check = self.client.get(
            reverse("shopping-cart-list"),
            headers={"Authorization": f"Bearer {token2}"},
        )
        self.assertEqual(resp2_check.json()[0]["quantity"], 2)
