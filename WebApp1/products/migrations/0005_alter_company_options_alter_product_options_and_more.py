# Generated by Django 5.1.3 on 2024-11-19 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_status_alter_product_options_productinstance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Компания', 'verbose_name_plural': 'Компании'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterModelOptions(
            name='productinstance',
            options={'verbose_name': 'Экземпляр продукта', 'verbose_name_plural': 'Экземпляры продуктов'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
    ]
