# Generated by Django 2.0.2 on 2018-03-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20180312_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='palavras_chaves',
            field=models.TextField(blank=True, null=True, verbose_name='Palavra chaves'),
        ),
    ]
