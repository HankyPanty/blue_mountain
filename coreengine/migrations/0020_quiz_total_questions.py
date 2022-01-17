# Generated by Django 3.2.4 on 2022-01-17 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreengine', '0019_auto_20220117_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='total_questions',
            field=models.IntegerField(choices=[(16, '16'), (15, '15'), (14, '14'), (13, '13'), (12, '12'), (11, '11')], default=11),
            preserve_default=False,
        ),
    ]