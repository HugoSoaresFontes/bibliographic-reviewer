# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from base.views import BaseFormView, BaseTemplateView, BaseUpdateView, BaseListView
from .models import Revisao, Documento, Fichamento
from .forms import RevisaoForm
from base.mixins import LoginRequiredMixin, GroupRequiredMixin
from .importar_arquivos import importar_arquivos
class IndexView(LoginRequiredMixin, BaseTemplateView):
    template = 'main/index.html'
    titulo_pagina = "Início"
    subtitulo_pagina = "Dashboard"


class SucessoView(BaseTemplateView):
    template_name = 'sucesso.html'


class CadastroRevisaoView(GroupRequiredMixin, BaseFormView):
    titulo_pagina = "Revisão"
    model = Revisao
    form_class = RevisaoForm


class EdicaoRevisaoView(CadastroRevisaoView, BaseUpdateView):
    pass


class ListaRevisoesView(GroupRequiredMixin, BaseListView):
    template_name = 'main/listas/revisoes.html'
    titulo_pagina = "Revisões"
    model = Revisao
    queryset = Revisao.objects.filter()


class ListaDocumentosRevisaoView(GroupRequiredMixin, BaseListView):
    template_name = 'main/listas/artigos_revisao.html'
    titulo_pagina = "Documentos"
    model = Documento
    queryset = Documento.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(ListaDocumentosRevisaoView, self).get_context_data(**kwargs)
        context.update({'revisao': get_object_or_404(Revisao, id=self.kwargs['pk'])})
        self.queryset = Documento.objects.filter(revisao=kwargs.get('pk'))
        return context


class ImportarDocumentosView(ListaDocumentosRevisaoView):

    def get_context_data(self, **kwargs):
        context = super(ListaDocumentosRevisaoView, self).get_context_data(**kwargs)
        importar_arquivos(get_object_or_404(Revisao, id=self.kwargs['pk']), "IEEE Xplore")
        context.update({'revisao': get_object_or_404(Revisao, id=self.kwargs['pk'])})
        self.queryset = Documento.objects.filter(revisao=kwargs.get('pk'))
        return context