# Generated by Django 3.0.4 on 2020-04-01 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20200401_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='azurepersongroup',
            name='branch',
            field=models.CharField(choices=[('Comp', 'Computer'), ('Mech', 'Mechanical'), ('IT', 'Information Technology'), ('Elect', 'Electrical'), ('EC', 'Electronic and communication')], max_length=30),
        ),
    ]