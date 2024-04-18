# Generated by Django 5.0.4 on 2024-04-17 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0002_rename_user_id_shoppingcart_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shoppingcart",
            name="products",
            field=models.ManyToManyField(
                blank=True, null=True, through="payment.CartItem", to="payment.product"
            ),
        ),
    ]