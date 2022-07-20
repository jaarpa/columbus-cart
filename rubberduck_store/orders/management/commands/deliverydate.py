from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        orders = list(
            Order.objects.filter(estimated_delivery_date__isnull=True)
        )
        delivery_date = timezone.now() + timezone.timedelta(days=15)
        for order in orders:
            order.estimated_delivery_date = delivery_date
        Order.objects.bulk_update(orders, ["estimated_delivery_date"])
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully adding delivery date to %s orders" % len(orders)
            )
        )
