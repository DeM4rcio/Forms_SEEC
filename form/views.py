import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RespostaUnica
from .forms import FormularioEscolha
import os
from ldap3 import Server, Connection, NTLM, SUBTREE, ALL_ATTRIBUTES
from django.conf import settings

# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ldap3 import Server, Connection, NTLM, ALL, SUBTREE, ALL_ATTRIBUTES
from ldap3.core.exceptions import LDAPBindError, LDAPExceptionError

# Configurações de conexão (exemplo, substitua pelos seus valores reais)
# Certifique-se de que estas variáveis de ambiente estão configuradas corretamente


def login_view(request):
    return render(request, 'login.html')

@csrf_exempt
def autenticar_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('Email')
        senha = data.get('Senha')

        if not email or not senha:
            return JsonResponse({'success': False, 'message': 'Email e senha são obrigatórios.'}, status=400)

        # 1. Determinar o domínio e as configurações do servidor
        if "@economia.df.gov.br" in email:
            dominio = "SEAP"
            ldap_server = Server(settings.LDAP_SERVER, get_info=ALL)
            base_dn = 'dc=seap,dc=gdfnet,dc=df'
            servico_user = f"{dominio}\\{settings.LDAP_USERNAME.split('@')[0]}"
            servico_pass = settings.LDAP_PASSWORD
        elif "@gdfnet.df.gov.br" in email:
            dominio = "GDFNET"
            ldap_server = Server(settings.LDAP_SERVER_NET, get_info=ALL)
            base_dn = 'dc=gdfnet,dc=df'
            servico_user = f"{dominio}\\{settings.LDAP_USERNAME_NET.split('@')[0]}"
            servico_pass = settings.LDAP_PASSWORD_NET
        else:
            return JsonResponse({'success': False, 'message': 'Domínio de e-mail não reconhecido.'}, status=400)

        # 2. Conexão com o usuário de serviço para buscar o DN do usuário
        with Connection(
            ldap_server,
            user=servico_user,
            password=servico_pass,
            authentication=NTLM,
            auto_bind=True
        ) as conn:
            conn.search(
                search_base=base_dn,
                search_filter=f'(sAMAccountName={email.split("@")[0]})',
                search_scope=SUBTREE,
                attributes=ALL_ATTRIBUTES
            )

            if not conn.entries:
                return JsonResponse({'success': False, 'message': 'Usuário não encontrado.'}, status=404)

            user_entry = conn.entries[0]
            user_dn = user_entry.entry_dn

        # 3. Tentativa de autenticação com a senha do usuário
        try:
            with Connection(
                ldap_server,
                user=user_dn,
                password=senha,
                auto_bind=True
            ) as user_conn:
                # Se chegou aqui, a autenticação foi bem-sucedida
                user_info = {
                    "Email": user_entry.mail.value if "mail" in user_entry else None,
                    "Nome": user_entry.cn.value if "cn" in user_entry else None
                }
                return JsonResponse(user_info, status=200)

        except LDAPBindError:
            # Erro de autenticação, senha incorreta
            return JsonResponse({'success': False, 'message': 'Credenciais inválidas.'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Formato de requisição JSON inválido.'}, status=400)
    except LDAPExceptionError as e:
        print("Erro de LDAP:", e)
        return JsonResponse({'success': False, 'message': f'Erro de conexão com o servidor LDAP: {e}'}, status=500)
    except Exception as e:
        print("Erro na autenticação:", e)
        return JsonResponse({'success': False, 'message': 'Erro interno ao autenticar. Tente novamente mais tarde.'}, status=500)

@login_required(login_url='login')  
def formulario_view(request):
    try:
        resposta = RespostaUnica.objects.get(usuario=request.user)
        return render(request, "formulario.html", {"resposta": resposta, "respondido": True})
    except RespostaUnica.DoesNotExist:
        if request.method == "POST":
            # Aqui, o request.user já estará disponível
            form = FormularioEscolha(request.POST)
            if form.is_valid():
                nova_resposta = form.save(commit=False)
                nova_resposta.usuario = request.user
                nova_resposta.save()
                return redirect("formulario")
        else:
            form = FormularioEscolha()
        return render(request, "formulario.html", {"form": form, "respondido": False})
