# Generated by Django 3.2.5 on 2021-08-04 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210804_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemadetails',
            name='order',
            field=models.PositiveSmallIntegerField(),
        ),
    ]