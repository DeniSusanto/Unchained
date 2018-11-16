# Generated by Django 2.1.3 on 2018-11-16 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_order_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinicmanager',
            name='image',
        ),
        migrations.RemoveField(
            model_name='dispatcher',
            name='image',
        ),
        migrations.RemoveField(
            model_name='hospitalauthority',
            name='image',
        ),
        migrations.RemoveField(
            model_name='warehousepersonnel',
            name='image',
        ),
        migrations.AlterField(
            model_name='clinic',
            name='name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]