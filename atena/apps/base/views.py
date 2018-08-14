# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.db import transaction

from base.diggpagination import DiggPaginator as Paginator
from .mixins import *


class BaseTemplateView(TemplateView):
    template = ""
    titulo_pagina = ""
    subtitulo_pagina = ""

    def get_context_data(self, **kwargs):
        self.template_name = self.template
        context = super(BaseTemplateView, self).get_context_data(**kwargs)
        context['titulo_pagina'] = self.titulo_pagina
        context['subtitulo_pagina'] = self.subtitulo_pagina

        return context


class BaseFormView(LoginRequiredMixin, CreateView):
    template_name = 'main/cadastro.html'
    subtitulo_pagina = 'Cadastrar'
    success_url = '/sucesso/'

    def get_context_data(self, **kwargs):
        context = super(BaseFormView, self).get_context_data(**kwargs)
        context['titulo_pagina'] = self.titulo_pagina
        context['subtitulo_pagina'] = self.subtitulo_pagina
        return context

    def get_form_kwargs(self):
        kwargs = super(BaseFormView, self).get_form_kwargs()
        kwargs.update({'usuario': self.request.user})

        return kwargs

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super(BaseFormView, self).post(request, *args, **kwargs)


class BaseUpdateView(BaseFormView, UpdateView):
    subtitulo_pagina = ''

    def post(self, request, *args, **kwargs):
        if request.POST.get('reset', None) == 'Excluir':
            self.get_object().delete()
            return HttpResponseRedirect(self.success_url)

        else:
            return super(BaseUpdateView, self).post(request, *args, **kwargs)


class BaseListView(LoginRequiredMixin, TemplateView):
    template_name = "base/lista.html"
    subtitulo_pagina = "Lista"
    filtro = None
    entrada_atual_filtro = ""
    queryset = []
    paginate_by = 64
    titulo_pagina = ""

    def get_queryset(self):
        return self.queryset

    def get(self, *args, **kwargs):
        if self.filtro:
            filtro = self.filtro(self.request.GET or None, queryset=self.get_queryset())
            if filtro.is_valid():
                self.queryset = filtro.pesquisar()
                self.entrada_atual_filtro = filtro['entrada'].value()
            else:
                self.queryset = self.get_queryset()

        return super(BaseListView, self).get(*args, **kwargs)


    def get_context_data(self, **kwargs):
        paginator = Paginator(self.get_queryset(), self.paginate_by, tail=4, body=3)
        pagina = self.request.GET.get('pagina', 1)

        try:
            lista = paginator.page(pagina)
        except PageNotAnInteger:
            lista = paginator.page(1)
        except EmptyPage:
            lista = paginator.page(paginator.num_pages)

        GET_params = self.request.GET.copy()
        if 'pagina' in GET_params.keys():
            del GET_params['pagina']

        return {
            'GET_params': GET_params,
            'lista': lista,
            'filtro': self.filtro,
            'entrada_atual_filtro': self.entrada_atual_filtro,
            'titulo_pagina': self.titulo_pagina,
        }
