from django.contrib import admin
from safekey.models import User
from django import forms

# Criação do formulário para personalizar senha
class UserAdminForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput, label = "password") # Definindo senha como password para ela n ser exibida

    class Meta:
        model = User
        fields = "__all__" # Inclui todos os campos do modelo do formulário

class Users(admin.ModelAdmin):
    form = UserAdminForm # Usa o formulário personalizado
    list_display = ('id', 'name', 'email') # Exibe esses campos na listagem do admin
    list_display_links = ('id',) # Ao clicar no campo irá direcionar para poder editar os dados do usuário
    list_per_page = 10 # Exibir 10 usuários por pagina
    search_fields = ('name',) # Pesquisa pelo nome do usuário

admin.site.register(User, Users)