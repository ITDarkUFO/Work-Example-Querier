# Generated by Django 4.1 on 2022-08-30 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0010_alter_curatorskid_curator_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curatorskid',
            options={'ordering': ['curator', 'date_start', 'date_end'], 'verbose_name': 'куратор КИД', 'verbose_name_plural': 'кураторы КИД'},
        ),
        migrations.AlterField(
            model_name='curatorskid',
            name='curator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curator', to='server.person', verbose_name='Куратор'),
        ),
        migrations.AlterField(
            model_name='curatorskid',
            name='dependants',
            field=models.ManyToManyField(related_name='dependants', to='server.person', verbose_name='Подчиненные'),
        ),
    ]
