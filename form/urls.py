from django.urls import path

from form.views import formulario_view, autenticar_usuario, login_view


urlpatterns = [
    path("formulario/", formulario_view, name="formulario"),
    path('login', login_view, name='login'),
    path('autenticar_usuario/', autenticar_usuario, name='autenticar_usuario'),
]