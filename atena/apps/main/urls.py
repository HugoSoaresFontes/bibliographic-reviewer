# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^sucesso/$', SucessoView.as_view(), name='Sucesso'),
    url(r'^revisao/add/$', CadastroRevisaoView.as_view(), name='CadastroRevisao'),
    url(r'^revisao/lista/$', ListaRevisoesView.as_view(), name='ListaRevisoes'),
    url(r'^revisao/(?P<pk>\d+)/$', EdicaoRevisaoView.as_view(), name='EdicaoRevisao'),
    url(r'^revisao/(?P<pk>\d+)/artigos$', ListaDocumentosRevisaoView.as_view(), name='ListaDocumentosRevisao'),

    url(r'^revisao/(?P<pk>\d+)/documentos/importar/$', ImportarDocumentosView.as_view(), name='ImportarDocumentos'),
    url(r'^revisao/(?P<pk>\d+)/documentos/remover/$', RemoverDocumentoRevisaoView.as_view(), name='RemoverDocumentos'),
    url(r'^revisao/(?P<pk>\d+)/documentos/classificar/$', ClassificarDocumentosView.as_view(), name='ClassificarDocumentos'),
    url(r'^revisao/(?P<revisao_pk>\d+)/documento/fichamento/add/(?P<documento_pk>\d+)$',
    	CadastroFichamentoView.as_view(), name='CadastroFichamento'),
    url(r'^revisao/(?P<revisao_pk>\d+)/documento/(?P<documento_pk>\d+)/fichamento/(?P<pk>\d+)$', 
    	EdicaoFichamentoView.as_view(), name='EdicaoFichamento'),

    url(r'^revisao/(?P<revisao_pk>\d+)/documentos/tags/add/$', CadastroTagView.as_view(), name='CadastroTag'),

]