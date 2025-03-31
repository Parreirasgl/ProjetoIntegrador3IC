from django.core.exceptions import ValidationError
from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=64)
    ativo = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.nome

    def clean(self):
        super().clean()  # Chama o método clean da classe pai
        if Usuario.objects.filter(email=self.email).exists():
            raise ValidationError('Email já existe!')