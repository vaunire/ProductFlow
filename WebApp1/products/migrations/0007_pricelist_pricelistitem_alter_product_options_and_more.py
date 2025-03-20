# Generated by Django 5.1.6 on 2025-03-18 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productinstance_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Номер прайс-листа')),
                ('data', models.DateField(verbose_name='Дата утверждения')),
            ],
            options={
                'verbose_name': 'Прайс-лист',
                'verbose_name_plural': 'Прайс-листы',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='PriceListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_product', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Цена продукта в прайс-листе')),
            ],
            options={
                'verbose_name': 'Позиция прайс-листа',
                'verbose_name_plural': 'Позиции прайс-листов',
                'ordering': ['product_name'],
            },
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['company'], 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='images', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=120, null=True, verbose_name='URL-продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.company', verbose_name='Компания поставщик'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['id', 'slug'], name='products_pr_id_a08e3c_idx'),
        ),
        migrations.AddField(
            model_name='pricelistitem',
            name='number_pricelist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.pricelist', verbose_name='Номер прайс-листа'),
        ),
        migrations.AddField(
            model_name='pricelistitem',
            name='product_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='Название продукта'),
        ),
    ]
