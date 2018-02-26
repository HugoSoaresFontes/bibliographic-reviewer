# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect

from base.views import BaseFormView, BaseTemplateView, BaseUpdateView, BaseListView
from base.mixins import LoginRequiredMixin, GroupRequiredMixin
from .models import Revisao, Documento, Fichamento
from .importar_arquivos import importar_arquivos
from .forms import RevisaoForm

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
        self.queryset = Documento.objects.filter(revisoes=kwargs.get('pk'))
        return context


class ImportarDocumentosView(ListaDocumentosRevisaoView):

    def get(self,  request, *args, **kwargs):
        importar_arquivos(
            revisao=get_object_or_404(Revisao, id=kwargs['pk']), 
            base="IEEE Xplore",
            cadastrante=self.request.user
        )
        
        return HttpResponseRedirect(reverse('main:ListaDocumentosRevisao', kwargs={'pk':kwargs['pk']}))
        