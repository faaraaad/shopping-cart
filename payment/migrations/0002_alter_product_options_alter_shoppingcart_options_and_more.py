# Generated by Django 5.0.4 on 2024-04-18 23:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "کالا", "verbose_name_plural": "کالاها"},
        ),
        migrations.AlterModelOptions(
            name="shoppingcart",
            options={"verbose_name": "سبدخرید"},
        ),
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddIndex(
            model_name="cartitem",
            index=models.Index(
                fields=["product"], name="payment_car_product_58a91c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="cartitem",
            index=models.Index(fields=["cart"], name="payment_car_cart_id_02ceaf_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["title"], name="payment_pro_title_9a54c4_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["category"], name="payment_pro_categor_7368fc_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["price"], name="payment_pro_price_dbe68b_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["rating"], name="payment_pro_rating_537849_idx"),
        ),
        migrations.AddIndex(
            model_name="shoppingcart",
            index=models.Index(fields=["user"], name="payment_sho_user_id_9f7eaa_idx"),
        ),
    ]