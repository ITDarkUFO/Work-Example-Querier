# Generated by Django 4.1 on 2022-09-05 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0015_rename_deputy_governor_deputygovernor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Minister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.OneToOneField(default=None, error_messages={'unique': 'Этот сотрудник уже есть в таблице исполнителей КИД.'}, help_text='Министр, который будет будет отображаться в отчете КИД.', on_delete=django.db.models.deletion.CASCADE, to='server.person', verbose_name='Министр')),
            ],
            options={
                'verbose_name': 'министр',
                'verbose_name_plural': 'министры',
                'ordering': ['person'],
            },
        ),
    ]