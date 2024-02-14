# Generated by Django 4.1 on 2024-02-10 12:48

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userbase',
            options={'verbose_name': 'account', 'verbose_name_plural': 'accounts'},
        ),
        migrations.AlterField(
            model_name='userbase',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='userbase',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
