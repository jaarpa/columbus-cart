"""rubberduck_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from inventory import views as inventory_views
from carts import views as carts_views
from orders import views as orders_views

router = routers.DefaultRouter()
router.register(r"products", inventory_views.ProductsViewSet)
router.register(r"cart", carts_views.CartViewSet, basename="cart")
router.register(r"orders", orders_views.OrderViewset, basename="order")
router.register(r"sales", orders_views.SalesViewset, basename="sales")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/", include(router.urls)),
    path(
        "openapi/",
        get_schema_view(title="Rubber duck store API", version="1.0.0"),
        name="openapi-schema",
    ),
]
