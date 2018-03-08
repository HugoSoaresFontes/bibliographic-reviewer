# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from contas.models import Usuario
from base.models import BaseModel
import reversion


#data_conferencia=)
class Base(models.Model):
    # Constantes apontam para o ID de cada classe (preenchidas automaticamente por uma fixture)
    IEEE_XPLORE = 1
    SCIENCE_DIRECT = 2
    SCOPUS = 3
    PUBMED = 4
    PMC = 5
    WEB_OF_SCIENCE = 6
    SPRINGER = 7

    nome = models.CharField("Nome", max_length=255)

    class Meta:
        db_table = 'main_bases'
        verbose_name = 'Base'
        verbose_name_plural = 'Base'

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome

@reversion.register()
class Documento(BaseModel):
    """ Documentos das revisões  """
    bases = models.ManyToManyField(Base)

    titulo = models.CharField("Titulo", max_length=2048)
    resumo = models.TextField("Resumo")
    resumo_url = models.TextField("URL Resumo", null=True, blank=True)
    autores = models.TextField("Autores", null=True, blank=True)
    revista = models.CharField("Revista", max_length=255, null=True, blank=True)
    citado_papers = models.IntegerField("Número de papers que citaram o artigo",
                                        null=True, blank=True)
    citado_patentes = models.IntegerField("Número de patentes que citaram o artigo",
                                         null=True, blank=True)
    doi = models.CharField("DOi", max_length=255, null=True, blank=True)

    html_url = models.CharField("Nome completo de um autor", max_length=255,
                                null=True, blank=True)
    palavras_chaves = models.TextField("Termos do autor e da revista", null=True, blank=True)

    pdf_url	= models.CharField("URL do pdf", max_length=255, null=True, blank=True)
    data = models.DateField("Data da publicação", null=True, blank=True)
    rank = models.IntegerField("Rank do artigo na pesquisa", null=True, blank=True)
    citado_papers_scholar = models.IntegerField("Número de citações pelo Google Scholar", null=True, blank=True)
    citado_papers_scholar_data = models.DateTimeField("Rank do artigo na pesquisa", null=True, blank=True)

    arquivo = models.FileField(
        upload_to='arquivos', verbose_name='Arquivo do documento')

    class Meta:
        db_table = 'main_documentos'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        unique_together = (("titulo", "doi"),)

    @property
    def lista_fichamentos_revisoes(self):
        return list(Fichamento.objects.filter(documento=self.id).values_list('revisao__id', flat=True))

    @property
    def dicionario_fichamentos_revisoes(self):
        fichamentos = Fichamento.objects.filter(documento=self.id).values_list('revisao__id', 'id')
        if fichamentos: 
            return dict(fichamentos)

    @property
    def bases_string(self):
        return ','.join([a.nome for a in self.bases.all()])

    def __unicode__(self):
        return self.titulo

    def __str__(self):
        return self.titulo

@reversion.register()
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


class Tag(BaseModel):
    nome = models.CharField("Nome", max_length=20)
    cor = models.CharField("Cor", max_length=7)

    revisao = models.ForeignKey(Revisao, on_delete=models.CASCADE)


    class Meta:
        db_table = 'main_tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tag'

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome


@reversion.register()
class Fichamento(BaseModel):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name="fichamentos")
    revisao = models.ForeignKey(Revisao, on_delete=models.CASCADE, related_name="fichamentos")
    caracteristicas_dados = models.TextField("Características dos dados analisados", blank=True)
    citacoes = models.TextField("Citações", blank=True)
    anotacoes = models.TextField("Anotações gerais", blank=True)

    tags = models.ManyToManyField(Tag, related_name='fichamentos')

    class Meta:
        db_table = 'main_fichamentos'
        verbose_name = 'fichamentos'
        verbose_name_plural = 'fichamentos'

    def __unicode__(self):
        return self.documento.titulo

    def __str__(self):
        return self.documento.titulo 