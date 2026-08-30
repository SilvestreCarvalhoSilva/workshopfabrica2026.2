
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome




class Produto(models.Model):
    nome = models.CharField(max_length=80)

    descricao = models.TextField(
        blank=True,
        null=True
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantidade = models.IntegerField()

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

    imagem = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to='produtos/videos/',
        blank=True,
        null=True
    )