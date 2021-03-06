# Generated by Django 3.2.4 on 2021-08-14 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreengine', '0004_auto_20210620_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherpersonalinfo',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='student',
            name='classroom',
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(blank=True, help_text='Select all students to be present here', to='coreengine.Student'),
        ),
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='contact_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='emergenct_contact',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='fathers_last_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='fathers_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='heightCM',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='mothers_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='weight',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='aadhar_no',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='blood_group',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='contact_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='emergenct_contact',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='fee',
            name='classroom',
            field=models.ForeignKey(blank=True, help_text='Select Only ONE', null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreengine.classroom'),
        ),
        migrations.AlterField(
            model_name='fee',
            name='financial_year',
            field=models.ForeignKey(blank=True, help_text='Select Only ONE', null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreengine.fy'),
        ),
        migrations.AlterField(
            model_name='fee',
            name='student',
            field=models.ForeignKey(blank=True, help_text='Select Only ONE', null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreengine.student'),
        ),
        migrations.DeleteModel(
            name='StudentPersonalInfo',
        ),
        migrations.DeleteModel(
            name='TeacherPersonalInfo',
        ),
    ]
