# app/forms.py
from django import forms
from .models import RespostaUnica

class FormularioEscolha(forms.ModelForm):
    class Meta:
       opcao = forms.ChoiceField(
        choices=RespostaUnica.OPCOES,
        widget=forms.RadioSelect,
        empty_label=None  # Adicione esta linha
    )

    class Meta:
        model = RespostaUnica
        fields = ['opcao'] 
