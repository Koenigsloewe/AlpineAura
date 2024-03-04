# Generated by Django 4.1 on 2024-02-28 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_user_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.ImageField(blank=True, help_text='Upload an image for the category', null=True, upload_to='category_images/', verbose_name='Category Image'),
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(blank=True, help_text='Upload an icon for the category', null=True, upload_to='category_icons/', verbose_name='Icon'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99 €'}}, help_text='Maximum 999.99', max_digits=5, verbose_name='Discount Price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='regular_price',
            field=models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 999.99 €'}}, help_text='Maximum 999.99', max_digits=5, verbose_name='Regular Price'),
        ),
    ]