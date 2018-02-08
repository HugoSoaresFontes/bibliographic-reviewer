# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from contas.models import Usuario
from base.models import BaseModel


class Revisao(BaseModel):
    """ Revisões Bibliográficas """
    nome = models.CharField("Nome", max_length=90)
    descricao = models.TextField("Descricao")
    usuarios = models.ManyToManyField(Usuario, related_name="revisoes")
    adm = models.ForeignKey(Usuario, related_name='adm_revisoes', on_delete=models.CASCADE)

    class Meta:
        db_table = 'main_revisoes'
        verbose_name = 'Revisão'
        verbose_name_plural = 'Revisões'

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome