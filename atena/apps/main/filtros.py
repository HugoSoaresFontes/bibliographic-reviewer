# -*- coding: utf -*-
from django import forms
from django.db.models import Q
from base.filtros import BaseFiltroForm


class ListaDocumentosRevisaoFiltro(BaseFiltroForm):
    entrada = forms.CharField(required=False, label='Pesquisar')

    def __init__(self, *args, **kwargs):
        return super(ListaDocumentosRevisaoFiltro, self).__init__(*args, **kwargs)

    def pesquisar(self):
        resposta = super(ListaDocumentosRevisaoFiltro, self).pesquisar()

        if self.cleaned_data['entrada'] != '':
            resposta = resposta.filter(
                Q(titulo__icontains=self.cleaned_data['entrada'])|
                Q(bases__nome__icontains=self.cleaned_data['entrada'])|
                Q(fichamentos__cadastrado_por__username__icontains=self.cleaned_data['entrada'])|
                Q(autores__icontains=self.cleaned_data['entrada'])
            )

        return resposta
