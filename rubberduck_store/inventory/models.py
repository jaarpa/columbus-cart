import uuid
from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.


class JournalEntry(models.Model):

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE)
    quantity = models.DecimalField(default=1, max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Entry")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("journalentry_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if self.product.stock <= 0:
            self.product.available = False
            self.product.save()
        elif not self.product.available:
            self.product.available = True
            self.save()


class Product(models.Model):

    barcode = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
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
        return reverse("product-detail", kwargs={"pk": self.pk})

    @property
    def stock(self) -> Decimal:
        computed_stock = JournalEntry.objects.filter(product=self).aggregate(
            models.Sum("quantity")
        )["quantity__sum"] or Decimal("0.00")
        return computed_stock


class ProductImage(models.Model):

    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images")

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def get_absolute_url(self):
        return reverse("productimage-detail", kwargs={"pk": self.pk})
