# Generated by Django 2.0.2 on 2018-02-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisao',
            name='documentos',
            field=models.ManyToManyField(related_name='revisoes', to='main.Documento'),
        ),
    ]
