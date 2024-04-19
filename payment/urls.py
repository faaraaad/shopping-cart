from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet, ProductAPIView
from django.urls import include, path


router = DefaultRouter()
router.register(r"", CartItemViewSet, basename="shopping-cart")

urlpatterns = [
    path("shopping_cart/", include(router.urls)),
    path("products/", ProductAPIView.as_view()),
]
