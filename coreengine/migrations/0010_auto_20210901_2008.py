# Generated by Django 3.2.4 on 2021-09-01 20:08

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coreengine', '0009_rename_financial_year_exammark_exam'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='wightage',
            new_name='weightage',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='exams',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='financial_year',
        ),
        migrations.RemoveField(
            model_name='exammark',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='exammark',
            name='total_marks',
        ),
        migrations.AddField(
            model_name='exam',
            name='classroom',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.PROTECT, to='coreengine.classroom'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.IntegerField(choices=[(8, 'GeneralKnolowdge'), (7, 'Computer'), (6, 'Science'), (5, 'Maths'), (4, 'History'), (3, 'Geography'), (2, 'Marathi'), (1, 'Hindi'), (0, 'English')], default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exam',
            name='total_marks',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='fee',
            name='add_to_future_students',
            field=models.IntegerField(choices=[(1, 'yes'), (0, 'no')], default=1, help_text='Applicable For Class level Fees'),
        ),
        migrations.AddField(
            model_name='student',
            name='grn_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='amount',
            name='fee',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='coreengine.fee'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='amount',
            name='student',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.PROTECT, to='coreengine.student'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='dob',
            field=models.DateField(default=datetime.date(2021, 9, 1)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1),
        ),
        migrations.CreateModel(
            name='AmountDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('amount_paid', models.IntegerField(default=0)),
                ('payement_type', models.IntegerField(choices=[(2, 'Card'), (1, 'Gpay'), (0, 'Cash')], default=0)),
                ('amount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coreengine.amount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
