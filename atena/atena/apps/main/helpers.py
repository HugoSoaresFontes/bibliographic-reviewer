# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Field, Submit, Div, Layout, HTML)
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