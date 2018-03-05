# Generated by Django 2.0.2 on 2018-03-05 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180302_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='doi',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='DOi'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='titulo',
            field=models.CharField(max_length=300, verbose_name='Titulo'),
        ),
        migrations.AlterUniqueTogether(
            name='documento',
            unique_together={('titulo', 'doi')},
        ),
    ]