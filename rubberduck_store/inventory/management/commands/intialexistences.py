from typing import Any

from django.core.management.base import BaseCommand
from inventory.models import Product, JournalEntry


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        journal_entries = []
        for product in Product.objects.filter(available=True):
            if not JournalEntry.objects.filter(product=product).exists():
                journal_entries.append(
                    JournalEntry(
                        user=product.seller,
                        product=product,
                        quantity=len(product.name),
                    )
                )
        JournalEntry.objects.bulk_create(journal_entries)
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully added stock to %s products"
                % len(journal_entries)
            )
        )
