# Generated by Django 2.0.1 on 2018-01-21 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicesession',
            name='finish',
            field=models.DateTimeField(null=True),
        ),
    ]