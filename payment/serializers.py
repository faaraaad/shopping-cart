from rest_framework import serializers
from .models import Product, CartItem, ShoppingCart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ShoppingCart
        fields = ["id", "product", "quantity"]
