# Generated by Django 2.1.2 on 2018-11-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20181105_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='orderLabel/'),
        ),
    ]
