# Generated by Django 4.0.2 on 2022-02-26 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_ordermaterial_material_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmpwork',
            name='work_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
