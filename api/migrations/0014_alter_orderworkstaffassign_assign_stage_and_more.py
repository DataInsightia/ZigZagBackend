# Generated by Django 4.0.2 on 2022-02-27 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_orderworkstaffassign_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderworkstaffassign',
            name='assign_stage',
            field=models.CharField(blank=True, choices=[('cutting', 'CUTTING'), ('stitching', 'STITCHING'), ('hook', 'HOOK'), ('overlock', 'OVERLOCK')], default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orderworkstaffassign',
            name='work',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='work_assigned', to='api.work'),
        ),
    ]
