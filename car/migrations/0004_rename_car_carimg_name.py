# Generated by Django 5.0.4 on 2024-04-26 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_remove_car_images_carimg'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carimg',
            old_name='car',
            new_name='name',
        ),
    ]
