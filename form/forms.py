# app/forms.py
from django import forms
from .models import RespostaUnica

class FormularioEscolha(forms.ModelForm):
    class Meta:
        model = RespostaUnica
        fields = ['opcao']
        widgets = {
            'opcao': forms.RadioSelect
        }
