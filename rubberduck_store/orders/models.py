from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.


class Order(models.Model):

    owner = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True
    )
    date_placed = models.DateTimeField(auto_now_add=True)
    estimated_delivery_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("order", kwargs={"pk": self.pk})


class OrderItem(models.Model):

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    journal_entry = models.ForeignKey(
        "inventory.JournalEntry", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return "{} ordered {} x {}".format(
            self.order.client.username,
            self.journal_entry.quantity,
            self.journal_entry.product.name,
        )

    def get_absolute_url(self):
        return reverse("order_item", kwargs={"pk": self.pk})
