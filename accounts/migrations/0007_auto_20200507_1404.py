# Generated by Django 3.0.3 on 2020-05-07 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200507_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Indoor', 'Indoor'), ('OutDoor', 'OutDoor')], max_length=255, null=True),
        ),
    ]
