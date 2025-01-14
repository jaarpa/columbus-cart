from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.


class CartItem(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE)
    quantity = models.DecimalField(default=1, max_digits=9, decimal_places=2)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart items")

    def __str__(self):
        return f"{self.quantity} {self.product.name}"

    def get_absolute_url(self):
        return reverse("cart-detail", kwargs={"pk": self.pk})
