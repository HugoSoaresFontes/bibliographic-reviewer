# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import FormView, RedirectView
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from django.utils.http import is_safe_url
from django.shortcuts import render

from base.views import BaseFormView, BaseUpdateView, TemplateView
from base.mixins import LoginRequiredMixin
from .forms import LoginForm, UsuarioForm
from .models import Usuario

class LoginView(FormView):
    template_name = 'contas/login.html'
    form_class = LoginForm
    success_url = '/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)

        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url

        return redirect_to

    def form_valid(self, form):
        if form.is_valid():
            if not form.cleaned_data['lembrar_me']:
                self.request.session.set_expiry(0)
            login(self.request, form.obter_usuario())
        return super(LoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, RedirectView):
    url = '/contas/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class CadastroUsuarioView(BaseFormView):
    titulo_pagina = "Usuário"
    subtitulo_pagina = 'Cadastrar'
    model = Usuario
    form_class = UsuarioForm


class EdicaoUsuarioView(CadastroUsuarioView, BaseUpdateView):
    subtitulo_pagina = 'Editar'

    def get_queryset(self):
        if self.request.user.has_group('Administrador'):
            return Usuario.objects.all()
        else:
            return Usuario.objects.filter(id=self.request.user.id)


class ProfileView(TemplateView):
    template_name = 'contas/profile.html'

    def get_object(self):
        return get_object_or_404(Usuario, id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        context.update({
            'obj': self.get_object(),
        })

        return context