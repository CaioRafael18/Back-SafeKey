from django.contrib import admin
from safekey.models import Usuario
from django import forms

# Criação do formulário para personalizar senha
class UsuarioAdminForm(forms.ModelForm):
    senha = forms.CharField(widget = forms.PasswordInput, label = "senha") # Definindo senha como password para ela n ser exibida

    class Meta:
        model = Usuario
        fields = "__all__" # Inclui todos os campos do modelo do formulário

class Usuarios(admin.ModelAdmin):
    form = UsuarioAdminForm # Usa o formulário personalizado
    list_display = ('id', 'nome', 'email') # Exibe esses campos na listagem do admin
    list_display_links = ('id',) # Ao clicar no campo irá direcionar para poder editar os dados do usuário
    list_per_page = 10 # Exibir 10 usuários por pagina
    search_fields = ('nome',) # Pesquisa pelo nome do usuário

admin.site.register(Usuario, Usuarios)