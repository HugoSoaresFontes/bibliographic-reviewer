# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from base.views import BaseFormView, BaseTemplateView, BaseUpdateView, BaseListView
from base.mixins import LoginRequiredMixin, GroupRequiredMixin
from django.views import View
from django.views.generic import FormView
from reversion.views import RevisionMixin

from .models import Revisao, Documento, Fichamento, Tag
from .importar_arquivos import importar_arquivos
from .forms import RevisaoForm, FichamentoForm, SelecionarBaseForm, TagForm, DocumentoForm
import scholarly
import json
from datetime import datetime
from django.db import transaction


class IndexView(LoginRequiredMixin, BaseTemplateView):
    template = 'main/index.html'
    titulo_pagina = "Início"
    subtitulo_pagina = "Dashboard"


class SucessoView(BaseTemplateView):
    template = 'sucesso.html'
    titulo_pagina = "Operação realizada com sucesso"


class VisualizaDocumentoView(LoginRequiredMixin, BaseTemplateView):
    template = 'main/documento.html'
    titulo_pagina = "Documento"
    subtitulo_pagina = "Visualização"

    def get_context_data(self, **kwargs):
        context = super(VisualizaDocumentoView, self).get_context_data(**kwargs)
        context.update({'revisao': get_object_or_404(Revisao, id=self.kwargs['pk'])})
        context.update({'documento': get_object_or_404(Documento, id=self.kwargs['pk_documento'])})
        try:
            context.update({'fichamento': Fichamento.objects.filter(documento=self.kwargs['pk_documento'],
                                                                    revisao__id=self.kwargs['pk']).get()})
        except Exception:
            pass

        return context


class CadastroRevisaoView(RevisionMixin, GroupRequiredMixin, BaseFormView):
    titulo_pagina = "Revisão"
    model = Revisao
    form_class = RevisaoForm

    def get_success_url(self):
        return reverse('main:ListaRevisoes')


class EdicaoRevisaoView(CadastroRevisaoView,RevisionMixin, BaseUpdateView):
    pass


class ListaRevisoesView(GroupRequiredMixin, BaseListView):
    template_name = 'main/listas/revisoes.html'
    titulo_pagina = "Revisões"
    model = Revisao

    def get_queryset(self):
        return Revisao.objects.filter(usuarios=self.request.user)


class CadastroDocumentoRevisaoView(RevisionMixin, GroupRequiredMixin, BaseFormView):
    titulo_pagina = "Documento"
    model = Documento
    form_class = DocumentoForm

    def get_success_url(self):
        return reverse('main:ListaDocumentosRevisao', kwargs={'pk': self.kwargs['revisao_pk']})

    def get_form_kwargs(self):
        kwargs = super(CadastroDocumentoRevisaoView, self).get_form_kwargs()
        kwargs['revisao'] = get_object_or_404(Revisao, id=self.kwargs['revisao_pk'])

        return kwargs


class ListaDocumentosRevisaoView(GroupRequiredMixin, BaseListView):
    template_name = 'main/listas/artigos_revisao.html'
    titulo_pagina = "Documentos"
    model = Documento

    def get_queryset(self):
        queryset = Documento.objects.filter(revisoes=self.kwargs.get('pk'))
        if self.request.GET.get('tag'):
            tags = self.request.GET.get('tag').split(',')
            queryset = queryset.filter(fichamentos__tags__id__in=tags)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListaDocumentosRevisaoView, self).get_context_data(**kwargs)
        context.update({'revisao': get_object_or_404(Revisao, id=self.kwargs['pk'])})
        context.update({'lista_tags': Tag.objects.filter(revisao=self.kwargs['pk'])})

        return context


class ClassificarDocumentosView(ListaDocumentosRevisaoView):

    def get(self, request, *args, **kwargs):
        docs = Documento.objects.filter(revisoes=kwargs.get('pk'), citado_papers_scholar=None)
        for doc in docs:
            item = next(scholarly.search_pubs_query(doc.doi), None)
            if item:
                with transaction.atomic():
                    try:
                        doc.citado_papers_scholar = item.citedby
                    except:
                        doc.citado_papers_scholar = -1
                    doc.citado_papers_scholar_data = datetime.utcnow()
                    doc.save()

        return HttpResponseRedirect(reverse('main:ListaDocumentosRevisao', kwargs={'pk': kwargs['pk']}))


class ImportarDocumentosView(RevisionMixin, FormView):
    template_name = 'main/selecionar_bases.html'
    form_class = SelecionarBaseForm
    titulo_pagina = "Importar artigos"

    def get_initial(self):
        return {'revisao': self.kwargs['pk']}

    def get_context_data(self, **kwargs):
        context = super(ImportarDocumentosView, self).get_context_data(**kwargs)
        context.update({'subtitulo_pagina': "Selecionar bases e termos de pesquisa"})
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        print(data)

        termos_tecnologia = [x.strip() for x in data['termos_de_tecnologias'].split(',')]
        termos_saude = [x.strip() for x in data['termos_da_saude'].split(',')]
        revistas = [x.strip() for x in data['revistas'].split(',')]

        for base in data['bases_de_pesquisa']:
            print(base)
            importar_arquivos(
                revisao=get_object_or_404(Revisao, id=data['revisao']),
                base=base,
                queryterms=[termos_tecnologia, termos_saude],
                cadastrante=self.request.user,
                ano_inicio=data.get('ano_inicio'),
                ano_fim=data.get('ano_fim'),
                revistas=revistas
            )

        return HttpResponseRedirect(reverse('main:ListaDocumentosRevisao', kwargs={'pk': data['revisao']}))


class RemoverDocumentoRevisaoView(RevisionMixin, View):
    def post(self, request, *args, **kwargs):
        revisao = get_object_or_404(Revisao, id=self.kwargs['pk'])
        docs_ids = request.POST.getlist('docs[]')
        docs = Documento.objects.filter(id__in=docs_ids)
        for doc in docs:
            revisao.documentos.remove(doc)
            Fichamento.objects.filter(documento=doc.id, revisao=revisao.id).delete()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class AssociarTagView(RevisionMixin, View):
    def post(self, request, *args, **kwargs):
        revisao = get_object_or_404(Revisao, id=self.kwargs['revisao_pk'])
        docs_ids = request.POST.getlist('docs[]')
        tag = get_object_or_404(Tag, id=request.POST.get('id'))
        docs = Documento.objects.filter(id__in=docs_ids)
        for doc in docs:
            fichamento, exists = Fichamento.objects.get_or_create(documento=doc, revisao=revisao)
            if fichamento.tags.filter(pk=tag.id).exists():
                fichamento.tags.remove(tag)
            else:
                fichamento.tags.add(tag)

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class CadastroFichamentoView(RevisionMixin, GroupRequiredMixin, BaseFormView):
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


class CadastroTagView(RevisionMixin, GroupRequiredMixin, BaseFormView):
    titulo_pagina = "Tag"
    model = Tag
    form_class = TagForm

    def get_form_kwargs(self):
        kwargs = super(CadastroTagView, self).get_form_kwargs()
        kwargs['revisao'] = get_object_or_404(Revisao, id=self.kwargs['revisao_pk'])

        return kwargs

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            return JsonResponse({'tag': {'nome': self.object.nome,
                                         'cor': self.object.cor,
                                         'id': self.object.id,
                                         }})


def handler400(request):
    return render(request, 'main/erros/400.html')


def handler404(request):
    return render(request, 'main/erros/404.html')


def handler403(request):
    return render(request, 'main/erros/403.html')


def handler500(request):
    return render(request, 'main/erros/500.html')
