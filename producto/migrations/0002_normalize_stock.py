from django.db import migrations


def forwards(apps, schema_editor):
    Producto = apps.get_model('producto', 'Producto')
    # Set any negative stock to zero
    for p in Producto.objects.filter(stock_producto__lt=0):
        p.stock_producto = 0
        p.save()


def reverse(apps, schema_editor):
    # No-op reverse: cannot restore previous negative stocks safely
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
