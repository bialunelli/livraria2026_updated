from django.db import models
from sympy import false


class Autor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)
    descricao = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        verbose_name = 'autor'
        verbose_name_plural = 'autores'

    def __str__(self):
        return self.nome
