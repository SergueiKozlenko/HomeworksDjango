# Generated by Django 3.1.2 on 2021-06-03 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0003_auto_20210603_1839'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={'ordering': ['-updated_at', '-created_at'], 'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AlterModelOptions(
            name='favorites',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
    ]
