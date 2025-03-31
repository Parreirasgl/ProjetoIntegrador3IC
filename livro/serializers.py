# livro/serializers.py
from rest_framework import serializers # type: ignore
from .models import Livros

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livros
        fields = ['obra', 'compositor', 'arranjador']  # Defina apenas os campos que quer compartilhar
