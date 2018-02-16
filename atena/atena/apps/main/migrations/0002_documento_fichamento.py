# Generated by Django 2.0.2 on 2018-02-09 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cadastrado_em', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastrado')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Data da última atualizacao')),
                ('resumo', models.TextField(verbose_name='Resumo')),
                ('resumo_url', models.TextField(blank=True, null=True, verbose_name='URL Resumo')),
                ('autores_ordem', models.TextField(blank=True, null=True, verbose_name='Número de cada autor')),
                ('autores_termos', models.TextField(blank=True, null=True, verbose_name='Termos fornecidos pelo autor que descrevem o documento')),
                ('autores', models.TextField(blank=True, null=True, verbose_name='Autores')),
                ('citado_papers', models.IntegerField(blank=True, null=True, verbose_name='Número de papers que citaram o artigo')),
                ('citing_patents', models.IntegerField(blank=True, null=True, verbose_name='Número de patentes que citaram o artigo')),
                ('data_conferencia', models.CharField(blank=True, max_length=255, null=True, verbose_name='Datas da conferência')),
                ('lugar_conferencia', models.CharField(blank=True, max_length=255, null=True, verbose_name='Lugar da conferência')),
                ('doi', models.CharField(blank=True, max_length=255, null=True, verbose_name='DOi')),
                ('nome_completo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome completo de um autor')),
                ('html_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome completo de um autor')),
                ('index_termos', models.TextField(blank=True, null=True, verbose_name='Termos do autor e da revista')),
                ('termos_revista', models.TextField(blank=True, null=True, verbose_name='Termos da revista')),
                ('is_numero', models.CharField(blank=True, max_length=255, null=True, verbose_name='Identificador interno na revista')),
                ('isbn', models.CharField(blank=True, max_length=255, null=True, verbose_name='International Standard Book Numbe')),
                ('issn', models.CharField(blank=True, max_length=8, null=True, verbose_name='International Standard Serial Number')),
                ('issue', models.CharField(blank=True, max_length=30, null=True, verbose_name='Número da edição da revista em que o artigo foi publicado')),
                ('pdf_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='URL do pdf')),
                ('data_publicacao', models.DateField(blank=True, null=True, verbose_name='Data da pubicação')),
                ('numero_publicacao', models.IntegerField(blank=True, null=True, verbose_name='Número da publicação')),
                ('titulo_publicacao', models.CharField(blank=True, max_length=255, null=True, verbose_name='Titulo da publicação')),
                ('editora', models.CharField(blank=True, max_length=255, null=True, verbose_name='Editora')),
                ('rank', models.IntegerField(blank=True, null=True, verbose_name='Rank do artigo na pesquisa')),
                ('titulo', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Titulo')),
                ('arquivo', models.FileField(upload_to='arquivos', verbose_name='Arquivo do documento')),
                ('cadastrado_por', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fichamento', models.ManyToManyField(to='main.Revisao')),
            ],
            options={
                'verbose_name_plural': 'Documentos',
                'db_table': 'main_documentos',
                'verbose_name': 'Documento',
            },
        ),
        migrations.CreateModel(
            name='Fichamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cadastrado_em', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastrado')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Data da última atualizacao')),
                ('caracteristicas_dados', models.TextField(blank=True, verbose_name='Características dos dados analisados')),
                ('citacoes', models.TextField(blank=True, verbose_name='Citações')),
                ('anotacoes', models.TextField(blank=True, verbose_name='Anotações gerais')),
                ('cadastrado_por', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fichamentos', to='main.Documento')),
                ('revisao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fichamentos', to='main.Revisao')),
            ],
            options={
                'verbose_name_plural': 'fichamentos',
                'db_table': 'main_fichamentos',
                'verbose_name': 'fichamentos',
            },
        ),
    ]
