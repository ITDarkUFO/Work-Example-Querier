# Generated by Django 4.1 on 2022-08-30 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0012_reportkid_pnc_coefficient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportkid',
            name='pnc_coefficient',
        ),
        migrations.RemoveField(
            model_name='reportkid',
            name='reports_completed_on_time_count',
        ),
        migrations.RemoveField(
            model_name='reportkid',
            name='reports_completed_out_time_count',
        ),
        migrations.RemoveField(
            model_name='reportkid',
            name='reports_count',
        ),
        migrations.RemoveField(
            model_name='reportkid',
            name='reports_incompleted_count',
        ),
    ]
