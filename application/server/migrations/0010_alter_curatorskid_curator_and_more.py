# Generated by Django 4.1 on 2022-08-30 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_alter_curatorskid_date_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curatorskid',
            name='curator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.person', verbose_name='Куратор'),
        ),
        migrations.AlterUniqueTogether(
            name='curatorskid',
            unique_together={('curator', 'date_start', 'date_end')},
        ),
    ]
