# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from base.views import BaseFormView, BaseTemplateView, BaseUpdateView
from base.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, BaseTemplateView):
    template = 'main/index.html'
    titulo_pagina = "Início"
    subtitulo_pagina = "Dashboard"


class SucessoView(BaseTemplateView):
    template_name = 'sucesso.html'