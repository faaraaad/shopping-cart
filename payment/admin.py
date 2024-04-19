from django.contrib import admin

from payment.models import Product, ShoppingCart, CartItem


@admin.register(Product, CartItem, ShoppingCart)
class ProductAdmin(admin.ModelAdmin):
    pass
