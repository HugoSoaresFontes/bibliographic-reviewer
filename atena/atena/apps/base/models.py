# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class BaseModel(models.Model):
    cadastrado_em = models.DateTimeField("Data de cadastrado", auto_now_add=True)
    cadastrado_por = models.ForeignKey('contas.Usuario', default=1, on_delete=models.CASCADE)
    atualizado_em = models.DateTimeField("Data da última atualizacao", auto_now=True)

    class Meta:
        abstract = True