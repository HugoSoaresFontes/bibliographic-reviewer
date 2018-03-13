# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate

from base.forms import *
from .helpers import *
from .models import *


class LoginForm(forms.Form):
    cpf = BRCPFFieldUnique(label='cpf', required=True)
    senha = forms.CharField(label='Senha', required=False)
    lembrar_me = forms.BooleanField(label="Manter conectado", required=False)

    def clean(self):
        if self.errors:
            return super(LoginForm, self).clean()

        usuarios = Usuario.objects.filter(cpf=self.cleaned_data['cpf'])
        self.usuario = authenticate(username=self.cleaned_data.get('cpf', None), password=self.cleaned_data['senha'])

        if usuarios.count() == 0:
            self.add_error('cpf', u'Nenhum usuário cadastrado com esse usuário')

        if (not self.usuario or not self.usuario.ativo == 1) and self.cleaned_data.get('cpf', None):
            self.add_error('senha', u'Senha incorreta')

        return super(LoginForm, self).clean()

    def obter_usuario(self):
        return self.usuario


class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(label=u'Senha', widget=forms.PasswordInput)
    senha2 = forms.CharField(label=u'Confirmação da senha', widget=forms.PasswordInput)
    imagem = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        exclude = ['password', 'ativo', 'admin', 'superusuario', 'last_login']

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.helper = UsuarioHelper()
        if self.instance.pk:
            self.fields['senha'].required = False
            self.fields['senha2'].required = False

    def clean_senha2(self):
        senha = self.cleaned_data["senha"]
        senha2 = self.cleaned_data["senha2"]
        if senha != senha2:
            raise forms.ValidationError(u"As senhas não são iguais")

    def save(self, commit=True):
        objeto = super(UsuarioForm, self).save(commit=False)
        if self.cleaned_data["senha"]:
            objeto.set_password(self.cleaned_data["senha"])

        if self.cleaned_data['imagem']:
            objeto.imagem = self.cleaned_data['imagem']

        if commit:
            objeto.save()

        return objeto