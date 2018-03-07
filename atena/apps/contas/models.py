# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin, Group)
from django.db import models

class Manager(BaseUserManager):
    def create_superuser(self, cpf, username, email, password):
        super_usuario = self.model(
            cpf=cpf,
            username=username,
            superusuario=True,
            admin=True,
            email=email
        )
        super_usuario.set_password(password)
        super_usuario.save(using=self.db)

        return super_usuario

    def create_user(self, cpf, username, email, password):
        super_usuario = self.model(
            cpf=cpf,
            username=username,
            email=email
        )
        super_usuario.set_password(password)
        super_usuario.save(using=self.db)


class Usuario(AbstractBaseUser, PermissionsMixin):
        ativo = models.BooleanField("Usuário Ativo?", default=True)
        cpf = models.CharField(max_length=11, verbose_name='CPF', unique=True)
        username = models.CharField(max_length=255, verbose_name='Nome pelo qual deseja ser tratado')
        email = models.EmailField(unique=True)

        imagem = models.ImageField(
            upload_to='imagens/contas', verbose_name='Imagem',
            null=True, blank=True
        )
        # admin do sistema
        admin = models.BooleanField(default=False)

        # Super user lais
        superusuario = models.BooleanField(default=False)

        objects = Manager()

        USERNAME_FIELD = 'cpf'
        REQUIRED_FIELDS = ['username', 'email']

        class Meta:
            db_table = 'contas_usuarios'
            verbose_name = 'Usuário'
            verbose_name_plural = 'Usuários'

        def __unicode__(self):
            return self.username

        def __str__(self):
            return self.username

        @property
        def is_active(self):
            return self.ativo

        @property
        def is_staff(self):
            return self.ativo == 1

        @property
        def is_superuser(self):
            return self.superusuario

        def get_short_name(self):
            return self.username

        def get_full_name(self):
            return self.username

        def has_group(self, group_name):
            group = Group.objects.get(name=group_name)
            return True if group in self.groups.all() else False