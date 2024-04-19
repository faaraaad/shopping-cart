from rest_framework.viewsets import GenericViewSet
from .models import ShoppingCart, Product, CartItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import CartItemSerializer, ProductSerializer
from rest_framework.response import Response
from django.db.models import F
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.generics import ListAPIView


class CartItemViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_or_create_shopping_cart(user) -> CartItem:
        return ShoppingCart.objects.get_or_create(user=user)[0]

    def list(self, request):
        """
        List all items in the shopping cart
        Require authenticated user to list its shopping cart products
        """
        cart_item = CartItem.objects.filter(cart__user=request.user)
        data = CartItemSerializer(instance=cart_item, many=True).data
        return Response(data)

    @action(url_path=r"add/(?P<product_id>\d+)", detail=False, methods=["post"])
    def add(self, request, product_id, *args, **kwargs):
        """
        Add a product to the shopping cart
        """
        product = Product.objects.get(id=product_id)
        if cart_item := CartItem.objects.filter(
            cart__user=request.user, product_id=product.id
        ):
            cart_item.update(quantity=F("quantity") + 1)
        else:
            shopping_cart = self.get_or_create_shopping_cart(request.user)
            shopping_cart.products.add(product)
            cart_item = CartItem.objects.filter(cart=shopping_cart)
        sz_data = CartItemSerializer(instance=cart_item, many=True).data
        return Response(sz_data, HTTP_201_CREATED)

    @action(url_path=r"remove/(?P<product_id>\d+)", detail=False, methods=["post"])
    def remove(self, request, product_id, *args, **kwargs):
        """
        Remove a product from the shopping cart
        """
        product = Product.objects.get(id=product_id)
        if cart_item := CartItem.objects.filter(
            cart__user=request.user, product_id=product.id
        ):
            quantity = cart_item.get().quantity
            if quantity > 1:
                cart_item.update(quantity=F("quantity") - 1)
            elif quantity == 1:
                shopping_cart = self.get_or_create_shopping_cart(request.user)
                shopping_cart.products.remove(product)
            else:
                return Response(status=HTTP_204_NO_CONTENT)
            sz_data = CartItemSerializer(instance=cart_item, many=True).data
            return Response(sz_data, HTTP_200_OK)
        return Response(status=HTTP_204_NO_CONTENT)


class ProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
