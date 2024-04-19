from django.contrib import admin
from django.urls import path, include
import utils.swagger

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/payment/", include("payment.urls")),
    path("api/authentication/", include("authentication.urls")),
    path("api/user/", include("user.urls")),
]

urlpatterns += utils.swagger.urlpatterns
