# Generated by Django 3.0.7 on 2020-08-26 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
