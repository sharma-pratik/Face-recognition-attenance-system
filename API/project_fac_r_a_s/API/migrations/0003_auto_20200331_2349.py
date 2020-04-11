# Generated by Django 3.0.4 on 2020-03-31 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20200331_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentattendance',
            old_name='total_subject_lectures',
            new_name='total_lectures',
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='total_lectures_taken',
            field=models.IntegerField(default=None),
        ),
    ]