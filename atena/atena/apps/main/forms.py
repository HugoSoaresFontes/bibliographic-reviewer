# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .helpers import RevisaoHelper, FichamentoHelper
from .models import Revisao, Documento, Fichamento
from base.forms import BaseForm


class RevisaoForm(BaseForm):

    class Meta:
        model = Revisao
        exclude = ['adm', 'documentos']

    def __init__(self, *args, **kwargs):
        super(RevisaoForm, self).__init__(*args, **kwargs)
        self.helper = RevisaoHelper()

    def save(self, commit=True):
        revisao = super(RevisaoForm, self).save(commit=False)
        revisao.adm = self.usuario
        if commit:
            revisao.save()
            self.save_m2m()


        return revisao


class FichamentoForm(BaseForm):

    class Meta:
        model = Fichamento
        exclude = ['documento', 'revisao']

    def __init__(self, *args, **kwargs):
        self.revisao = kwargs.pop('revisao')
        self.documento = kwargs.pop('documento')
        super(FichamentoForm, self).__init__(*args, **kwargs)
        self.helper = FichamentoHelper()

    def save(self, commit=True):
        fichamento = super(FichamentoForm, self).save(commit=False)
        fichamento.documento = self.documento
        fichamento.revisao = self.revisao
        
        if commit:
            fichamento.save()


        return fichamento