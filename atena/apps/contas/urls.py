from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'usuario/registrar-se/$', AutoCadastroUsuarioView.as_view(), name='autocadastro'),
    url(r'usuario/editar/(?P<pk>\d+)/$', EdicaoUsuarioView.as_view(),
        name='EdicaoUsuario'),
    url(r'usuario/profile/(?P<pk>\d+)/$', ProfileView.as_view(),
        name='Profile'),
]

