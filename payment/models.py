from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالاها"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["category"]),
            models.Index(fields=["price"]),
            models.Index(fields=["rating"]),
        ]

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    raters = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Title: {self.title} - Price: {self.price} - Category: {self.category}"


class ShoppingCart(models.Model):
    class Meta:
        verbose_name = "سبدخرید"
        verbose_name_plural = "سبدهای خرید"
        indexes = [
            models.Index(fields=["user"]),
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, null=True, blank=True, through="CartItem"
    )

    def __str__(self):
        return f"User: {self.user} - Products: {' - '.join([product.title for product in self.products.all()])}"


class CartItem(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["cart"]),
        ]

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Product: {self.product.title} - User: {self.cart.user.username} - Quantity: {self.quantity}"
