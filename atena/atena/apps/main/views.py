# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect

from base.views import BaseFormView, BaseTemplateView, BaseUpdateView, BaseListView
from base.mixins import LoginRequiredMixin, GroupRequiredMixin
from .models import Revisao, Documento, Fichamento
from .importar_arquivos import importar_arquivos
from .forms import RevisaoForm, FichamentoForm
import scholarly
from datetime import datetime

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

    def form_invalid(self, form):
        print(form.errors)


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


class ClassificarDocumentosView(ListaDocumentosRevisaoView):

    def get(self, request, *args, **kwargs):
        docs = Documento.objects.filter(revisoes=kwargs.get('pk'), citado_papers_scholar=None)
        for doc in docs[:2]:
            item = next(scholarly.search_pubs_query(doc.doi))
            if item:
                doc.citado_papers_scholar = item.citedby
                doc.citado_papers_scholar_data = datetime.utcnow()
                doc.save()

        return HttpResponseRedirect(reverse('main:ListaDocumentosRevisao', kwargs={'pk': kwargs['pk']}))


class ImportarDocumentosView(ListaDocumentosRevisaoView):

    def get(self,  request, *args, **kwargs):
        importar_arquivos(
            revisao=get_object_or_404(Revisao, id=kwargs['pk']), 
            base="Science Direct",
            cadastrante=self.request.user
        )
        
        return HttpResponseRedirect(reverse('main:ListaDocumentosRevisao', kwargs={'pk':kwargs['pk']}))
        

class CadastroFichamentoView(GroupRequiredMixin, BaseFormView):
    titulo_pagina = "Fichamento"
    model = Fichamento
    form_class = FichamentoForm

    def get_context_data(self, **kwargs):
        return super(CadastroFichamentoView, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(CadastroFichamentoView, self).get_form_kwargs()
        kwargs['revisao'] = get_object_or_404(Revisao, id=self.kwargs['revisao_pk'])
        kwargs['documento'] = get_object_or_404(Documento, id=self.kwargs['documento_pk'])

        return kwargs


class EdicaoFichamentoView(CadastroFichamentoView, BaseUpdateView):
    pass