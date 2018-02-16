# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Revisao, Documento, Fichamento
from .helpers import RevisaoHelper
from base.forms import BaseForm


class RevisaoForm(BaseForm):

    class Meta:
        model = Revisao
        exclude = ['adm']

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
