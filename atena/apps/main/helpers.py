# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Field, Submit, Div, Layout, HTML, Hidden)
from django.shortcuts import reverse


class RevisaoHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RevisaoHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('nome', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('descricao', rows=2,  css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('usuarios', css_class="form-control pesquisa select2-input"),
                css_class='form-group col-md-12'
            ),
            Div(
                Div(
                    Submit('submit', 'Salvar', css_class="btn pull-right"),
                    css_class='form-group col-md-12'
                ),
                css_class="row"
            )
        )


class DocumentoHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(DocumentoHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('titulo', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('doi', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('palavras_chaves', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('bases', css_class="form-control select2-input    "),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('autores',  rows=2, css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('revista', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('citado_papers', css_class="form-control"),
                css_class='form-group col-md-3'
            ),
            Div(
                Field('citado_patentes', css_class="form-control"),
                css_class='form-group col-md-3'
            ),
            Div(
                Field('citado_papers_scholar', css_class="form-control"),
                css_class='form-group col-md-3'
            ),
            Div(
                Field('citado_papers_scholar_data', css_class="form-control"),
                css_class='form-group col-md-3'
            ),
            Div(
                Field('html_url', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('resumo', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('resumo_url', required=False, rouws=1, css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('arquivo', required=False, rouws=1, css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            
            Div(
                Div(
                    Submit('submit', 'Salvar', css_class="btn pull-right"),
                    css_class='form-group col-md-12'
                ),
                css_class="row"
            )
        )


class FichamentoHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(FichamentoHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('tags', css_class="form-control select2-input"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('caracteristicas_dados', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('citacoes',  css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('anotacoes', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Div(
                    Submit('submit', 'Salvar', css_class="btn pull-right"),
                    css_class='form-group col-md-12'
                ),
                css_class="row"
            )
        )


class SelecionarBaseHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SelecionarBaseHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('termos_de_tecnologias', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('termos_da_saude',  css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('revistas',  css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Field('ano_inicio', css_class="form-control"),
                css_class='form-group col-md-6'
            ),
            Div(
                Field('ano_fim', css_class="form-control"),
                css_class='form-group col-md-6'
            ),
            Div(
                Field('bases_de_pesquisa', css_class=""),
                css_class='form-group col-md-12'
            )
            ,
            Div(
                Div(
                    Field('revisao'),
                    Submit('submit', 'Enviar', css_class="btn pull-right"),
                    css_class='form-group col-md-12'
                ),
                css_class="row"
            )
        )