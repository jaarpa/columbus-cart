# Generated by Django 4.0.6 on 2022-07-19 19:26

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    Product = apps.get_model("inventory", "Product")
    for row in Product.objects.all():
        row.barcode = uuid.uuid4()
        row.save(update_fields=["barcode"])


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0003_product_barcode"),
    ]

    operations = [
        migrations.RunPython(gen_uuid),
    ]
