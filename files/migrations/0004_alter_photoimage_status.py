# Generated by Django 3.2.4 on 2022-01-17 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_photo_photoimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photoimage',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1),
        ),
    ]
