from django.db import models

# Create your models here.
# app/models.py
from django.db import models
from django.contrib.auth.models import User

class RespostaUnica(models.Model):
    OPCOES = [
        ("conectaserv", "ConectaServ - Sua vida funcional na palma da mão"),
        ("gdfservidor", "GDF Servidor - Feito para quem trabalha pelo DF"),
        ("servigdf", "ServiGDF - O aplicativo do servidor do GDF"),
        ("gdfacil", "GDFácil - Mais agilidade para a vida do servidor do GDF"),
        ("meugdf", "MeuGDF - Feito para os servidores do DF"),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    opcao = models.CharField(max_length=20, choices=OPCOES)
    data_submissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_opcao_display()}"
