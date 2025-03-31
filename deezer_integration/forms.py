# deezer_integration/forms.py
from django import forms

class GenreForm(forms.Form):
    genre_choices = [
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
        ('pop', 'Pop'),
        ('metal', 'Metal'),
    ]
    genre = forms.ChoiceField(choices=genre_choices, label="Escolha um Gênero", required=True)
