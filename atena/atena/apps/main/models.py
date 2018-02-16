# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from contas.models import Usuario
from base.models import BaseModel


# class DocumentoManager(models.Manager):
#     def salvar_documento(self, titulo, resumo, resumo_url, data_publicacao=None, autores_ordem,
#                          autores=None, citado_papers=None, chaves_autores=None,
#                          citado_patentes=None, data_conferencia=None, lugar_conferencia=None,
#                          doi=None, nome_completo=None, html_url=None, palavras_chaves=None,
#                          chaves_revistas=None, is_numero=None, isbn=None, issn=None,
#                          issue=None, pdf_url=None, numero_publicacao, titulo_publicacao,
#                          editora=None, rank=None, arquivo=None):
#         documento = self.create(titulo=titulo, resumo=resumo, resumo_url=resumo_url,
#                                 data_publicacao=data_publicacao, autores_ordem=autores_ordem,
#                                 autores=autores, citado_papers=citado_papers, citado_patentes=citado_patentes,
#                                 data_conferencia=)

class Documento(BaseModel):
    """ Documentos das revisões  """
    resumo = models.TextField("Resumo")
    resumo_url = models.TextField("URL Resumo", null=True, blank=True)
    autores_ordem = models.TextField("Número de cada autor", null=True, blank=True)
    autores = models.TextField("Autores", null=True, blank=True)
    citado_papers = models.IntegerField("Número de papers que citaram o artigo",
                                        null=True, blank=True)
    citado_patentes = models.IntegerField("Número de patentes que citaram o artigo",
                                         null=True, blank=True)
    data_conferencia = models.CharField("Datas da conferência", max_length=255,
                                        null=True, blank=True)
    lugar_conferencia = models.CharField("Lugar da conferência", max_length=255,
                                         null=True, blank=True)
    doi = models.CharField("DOi", max_length=255, null=True, blank=True)
    nome_completo = models.CharField("Nome completo de um autor", max_length=255,
                                     null=True, blank=True)
    html_url = models.CharField("Nome completo de um autor", max_length=255,
                                null=True, blank=True)
    palavras_chaves = models.TextField("Termos do autor e da revista", null=True, blank=True)
    chaves_autores = models.TextField("Palavras chaves fornecidas pelo autor que descrevem o documento",
                                      null=True, blank=True)
    chaves_revista = models.TextField("Termos da revista", null=True, blank=True)
    is_numero = models.CharField("Identificador interno na revista", max_length=255,
                                 null=True, blank=True)
    isbn = models.CharField("International Standard Book Numbe", max_length=255,
                            null=True, blank=True)
    issn = models.CharField("International Standard Serial Number", max_length=8,
                            null=True, blank=True)
    issue = models.CharField("Número da edição da revista em que o artigo foi publicado",
                             max_length=30, null=True, blank=True)
    pdf_url	= models.CharField("URL do pdf", max_length=255, null=True, blank=True)
    data_publicacao = models.DateField("Data da pubicação", null=True, blank=True)
    numero_publicacao = models.IntegerField("Número da publicação", null=True, blank=True)
    titulo_publicacao = models.CharField("Titulo da publicação", max_length=255, null=True, blank=True)
    editora = models.CharField("Editora", max_length=255, null=True, blank=True)
    rank = models.IntegerField("Rank do artigo na pesquisa", null=True, blank=True)
    titulo = models.CharField("Titulo", max_length=255, null=True, blank=True, unique=True)

    arquivo = models.FileField(
        upload_to='arquivos', verbose_name='Arquivo do documento')

    class Meta:
        db_table = 'main_documentos'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

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
    documentos = models.ManyToManyField(Documento)

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
        return self.documento.titulo + " / " + self.revisao.titulo.nome

    def __str__(self):
        return self.documento.titulo + " / " + self.revisao.titulo.nome