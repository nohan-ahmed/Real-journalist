# Generated by Django 5.0.7 on 2024-09-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_awards_journalist_awards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalist',
            name='awards',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]