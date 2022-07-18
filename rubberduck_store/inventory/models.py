from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length=100)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seller_price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})


class ProductImage(models.Model):

    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images")

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def get_absolute_url(self):
        return reverse("product_image", kwargs={"pk": self.pk})