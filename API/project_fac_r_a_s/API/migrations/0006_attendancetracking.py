# Generated by Django 3.0.4 on 2020-03-16 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_periods_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Faculty')),
                ('periods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Periods')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
    ]
