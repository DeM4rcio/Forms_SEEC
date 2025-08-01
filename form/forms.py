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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove a primeira opção (vazia) do ChoiceField se ela existir
        if self.fields['opcao'].choices and self.fields['opcao'].choices[0][0] == '':
            self.fields['opcao'].choices = self.fields['opcao'].choices[1:]
