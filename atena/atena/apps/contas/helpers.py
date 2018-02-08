# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Field, Submit, Div, Layout)


class UsuarioHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(UsuarioHelper, self).__init__(*args, **kwargs)

        self.layout = Layout(
            Div(
                Field('username', css_class="form-control"),
                css_class='form-group col-md-6'
            ),
            Div(
                Field('email', css_class="form-control"),
                css_class='form-group col-md-6'
            ),
            Div(
                Field('senha', css_class="form-control"),
                css_class='form-group col-md-6'
            ),
            Div(
                Field('senha2', css_class="form-control"),
                css_class='form-group col-md-6'
            ),
            Div(
                Field('imagem', css_class="form-control"),
                css_class='form-group col-md-12'
            ),
            Div(
                Submit('submit', 'Confirmar', css_class="btn pull-right"),
                css_class='form-group col-md-12'
            ),
        )
