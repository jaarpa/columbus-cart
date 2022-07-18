from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.


class CartItem(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart items")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cart_item", kwargs={"pk": self.pk})
