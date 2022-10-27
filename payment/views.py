from django.shortcuts import get_object_or_404
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
    def get_or_create_shopping_cart(user) -> ShoppingCart:
        return ShoppingCart.objects.get_or_create(user=user)[0]

    def list(self, request):
        """
        List all items in the shopping cart
        Require authenticated user to list its shopping cart products
        """
        cart_items = CartItem.objects.filter(cart__user=request.user)
        data = CartItemSerializer(instance=cart_items, many=True).data
        return Response(data)

    @action(url_path=r"add/(?P<product_id>\d+)", detail=False, methods=["post"])
    def add(self, request, product_id, *args, **kwargs):
        """
        Add a product to the shopping cart
        """
        product = get_object_or_404(Product, id=product_id)
        shopping_cart = self.get_or_create_shopping_cart(request.user)
        
        cart_item, created = CartItem.objects.get_or_create(cart=shopping_cart, product=product)
        if not created:
            cart_item.quantity = F("quantity") + 1
            cart_item.save(update_fields=["quantity"])
            
        cart_items = CartItem.objects.filter(cart=shopping_cart)
        sz_data = CartItemSerializer(instance=cart_items, many=True).data
        return Response(sz_data, HTTP_201_CREATED)

    @action(url_path=r"remove/(?P<product_id>\d+)", detail=False, methods=["post"])
    def remove(self, request, product_id, *args, **kwargs):
        """
        Remove a product from the shopping cart
        """
        product = get_object_or_404(Product, id=product_id)
        shopping_cart = self.get_or_create_shopping_cart(request.user)
        
        try:
            cart_item = CartItem.objects.get(cart=shopping_cart, product=product)
        except CartItem.DoesNotExist:
            return Response(status=HTTP_204_NO_CONTENT)
            
        if cart_item.quantity > 1:
            cart_item.quantity = F("quantity") - 1
            cart_item.save(update_fields=["quantity"])
        else:
            cart_item.delete()
            
        cart_items = CartItem.objects.filter(cart=shopping_cart)
        sz_data = CartItemSerializer(instance=cart_items, many=True).data
        return Response(sz_data, HTTP_200_OK)


class ProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

