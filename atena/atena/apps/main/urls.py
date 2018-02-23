# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^revisao/add/$', CadastroRevisaoView.as_view(), name='CadastroRevisao'),
    url(r'^revisao/lista/$', ListaRevisoesView.as_view(), name='ListaRevisoes'),
    url(r'^revisao/(?P<pk>\d+)/$', EdicaoRevisaoView.as_view(), name='EdicaoRevisao'),
    url(r'^revisao/(?P<pk>\d+)/artigos$', ListaDocumentosRevisaoView.as_view(), name='ListaDocumentosRevisao'),

    url(r'^revisao/documentos/importar/(?P<pk>\d+)/$', ImportarDocumentosView.as_view(), name='ImportarDocumentos'),

]