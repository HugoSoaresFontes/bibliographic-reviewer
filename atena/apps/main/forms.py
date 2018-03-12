# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .helpers import RevisaoHelper, FichamentoHelper, SelecionarBaseHelper, DocumentoHelper
from .models import Revisao, Documento, Fichamento, Tag
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

            if self.usuario not in revisao.usuarios.all():
                revisao.usuarios.add(self.usuario)

        return revisao


class DocumentoForm(BaseForm):
    class Meta:
        model = Documento
        exclude = ['revisao']

    def __init__(self, *args, **kwargs):
        self.revisao = kwargs.pop('revisao')
        super(DocumentoForm, self).__init__(*args, **kwargs)
        self.helper = DocumentoHelper()

    def save(self, commit=True):
        documento = super(DocumentoForm, self).save(commit=False)
        

        if commit:
            documento.save()
            self.save_m2m()
            if self.revisao: 
                self.revisao.documentos.add(documento)

        return documento


class FichamentoForm(BaseForm):

    class Meta:
        model = Fichamento
        exclude = ['documento', 'revisao']

    def __init__(self, *args, **kwargs):
        self.revisao = kwargs.pop('revisao')
        self.documento = kwargs.pop('documento')
        super(FichamentoForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(revisao=self.revisao)
        self.helper = FichamentoHelper()


    def save(self, commit=True):
        fichamento = super(FichamentoForm, self).save(commit=False)
        fichamento.documento = self.documento
        fichamento.revisao = self.revisao
        
        if commit:
            fichamento.save()
            self.save_m2m()


        return fichamento


class TagForm(BaseForm):
    class Meta:
        model = Tag
        fields = ['nome', 'cor']

    def __init__(self, *args, **kwargs):
        self.revisao = kwargs.pop('revisao')
        super(TagForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        tag = super(TagForm, self).save(commit=False)
        tag.revisao = self.revisao

        if commit:
            tag.save()

        return tag


class SelecionarBaseForm(forms.Form):
    termos_de_tecnologias = forms.CharField(required=True)
    termos_da_saude = forms.CharField(required=True)
    revistas = forms.CharField(required=False)
    ano_inicio = forms.IntegerField(required=False)
    ano_fim = forms.IntegerField(required=False)
    bases_de_pesquisa = forms.MultipleChoiceField(
        choices=(
            ('IEEE Xplore', 'IEEE Xplore'),
            ('Scopus', 'Scopus'),
            ('Web of Science', 'Web of Science'),
            ('Springer', 'Springer'),
            ('Science Direct', 'Science Direct'),
            ('PMC', 'PMC'),
            ('PubMed', 'PubMed')
        ),
        widget=forms.CheckboxSelectMultiple()
    )
    revisao = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SelecionarBaseForm, self).__init__(*args, **kwargs)
        self.helper = SelecionarBaseHelper()

