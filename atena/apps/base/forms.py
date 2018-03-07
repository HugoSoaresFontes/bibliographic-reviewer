# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django import forms
from django.utils import timezone
from localflavor.br.forms import BRCPFField


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario')
        super(BaseForm, self).__init__(*args, **kwargs)
        if 'cadastrado_por' in self.fields:
            self.fields['cadastrado_por'].required = False

    def save(self, commit=True):
        objeto = super(BaseForm, self).save(commit=False)
        objeto.cadastrante = self.usuario
        if self.instance.id is not None:
            objeto.atualizado_em = timezone.now()

        if commit:
            objeto.save()
            self.save_m2m()

        return objeto


class BRCPFFieldUnique(BRCPFField):
    """
    Extende a classe BRCPFField para forçar valores
    únicos para o CPF e também para sempre salvar apenas
    os números na base de dados sem pontos e hífem.
    Usado no UserRegistrationForm que não extende o ModelForm
    e por isso ignora o fato do campo cpf estar marcado como único.
    """

    default_error_messages = {
        'invalid': "Número de CPF inválido.",
        'max_digits': "Este campo requer no máximo 11 dígitos ou 14 caracteres.",
    }

    def __init__(self, *args, **kwargs):
        super(BRCPFFieldUnique, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = re.sub("[-\.]", "", value)

        if value == '00000000000':
            return value

        super(BRCPFFieldUnique, self).clean(value)

        return value


class RGField(forms.CharField):

    def clean(self, value):
        value = str(value)
        value = re.sub("[()-\.]", "", value)
        return value


class TelefoneField(RGField):
    pass
