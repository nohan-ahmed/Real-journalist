# Generated by Django 5.0.7 on 2024-09-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]
