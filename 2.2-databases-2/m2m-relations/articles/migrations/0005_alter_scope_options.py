# Generated by Django 4.1.2 on 2022-11-01 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_scope_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scope',
            options={'verbose_name': 'Тематика статьи'},
        ),
    ]