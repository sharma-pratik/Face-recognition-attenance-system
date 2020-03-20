# Generated by Django 3.0.4 on 2020-03-15 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20200315_2359'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=100)),
                ('college_code', models.IntegerField()),
                ('gtu_afflicated', models.BooleanField()),
                ('domain', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='admin',
            name='full_name',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='CollegeManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('management_college_id', models.IntegerField()),
                ('email', models.EmailField(default=None, max_length=50)),
                ('password', models.CharField(default=None, max_length=50)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.College')),
            ],
        ),
    ]