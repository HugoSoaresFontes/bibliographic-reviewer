# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from contas.models import Usuario
from base.models import BaseModel


#data_conferencia=)
class Base(models.Model): 
    nome = models.CharField("Nome", max_length=255)

    class Meta:
        db_table = 'main_bases'
        verbose_name = 'Base'
        verbose_name_plural = 'Base'

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome


class Documento(BaseModel):
    """ Documentos das revisões  """
    bases = models.ManyToManyField(Base)

    titulo = models.CharField("Titulo", max_length=300, unique=True)
    resumo = models.TextField("Resumo")
    resumo_url = models.TextField("URL Resumo", null=True, blank=True)
    autores = models.TextField("Autores", null=True, blank=True)
    revista = models.CharField("Revista", max_length=255, null=True, blank=True)
    citado_papers = models.IntegerField("Número de papers que citaram o artigo",
                                        null=True, blank=True)
    citado_patentes = models.IntegerField("Número de patentes que citaram o artigo",
                                         null=True, blank=True)
    doi = models.CharField("DOi", max_length=255, null=True, blank=True, unique=True)

    html_url = models.CharField("Nome completo de um autor", max_length=255,
                                null=True, blank=True)
    palavras_chaves = models.TextField("Termos do autor e da revista", null=True, blank=True)

    pdf_url	= models.CharField("URL do pdf", max_length=255, null=True, blank=True)
    data = models.DateField("Data da pubicação", null=True, blank=True)
    rank = models.IntegerField("Rank do artigo na pesquisa", null=True, blank=True)

    arquivo = models.FileField(
        upload_to='arquivos', verbose_name='Arquivo do documento')

    class Meta:
        db_table = 'main_documentos'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    @property
    def lista_fichamentos_revisoes(self):
        return list(Fichamento.objects.filter(documento=self.id).values_list('revisao__id', flat=True))

    @property
    def dicionario_fichamentos_revisoes(self):
        fichamentos = Fichamento.objects.filter(documento=self.id).values_list('revisao__id', 'id')
        if fichamentos: 
            return dict(fichamentos)

    def __unicode__(self):
        return self.titulo

    def __str__(self):
        return self.titulo




class Revisao(BaseModel):
    """ Revisões Bibliográficas """
    nome = models.CharField("Nome", max_length=90)
    descricao = models.TextField("Descricao")
    usuarios = models.ManyToManyField(Usuario, related_name="revisoes")
    adm = models.ForeignKey(Usuario, related_name='adm_revisoes', on_delete=models.CASCADE)
    documentos = models.ManyToManyField(Documento, related_name='revisoes')

    class Meta:
        db_table = 'main_revisoes'
        verbose_name = 'Revisão'
        verbose_name_plural = 'Revisões'

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome


class Fichamento(BaseModel):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name="fichamentos")
    revisao = models.ForeignKey(Revisao, on_delete=models.CASCADE, related_name="fichamentos")
    caracteristicas_dados = models.TextField("Características dos dados analisados", blank=True)
    citacoes = models.TextField("Citações", blank=True)
    anotacoes = models.TextField("Anotações gerais", blank=True)

    class Meta:
        db_table = 'main_fichamentos'
        verbose_name = 'fichamentos'
        verbose_name_plural = 'fichamentos'


    def __unicode__(self):
        return self.documento.titulo

    def __str__(self):
        return self.documento.titulo 