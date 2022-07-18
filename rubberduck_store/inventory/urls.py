from django.urls import include, path
from rest_framework import routers
from inventory import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
