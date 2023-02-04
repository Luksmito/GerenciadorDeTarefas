from django.contrib import admin

from .models import Task


#Nesse arquivo precisamos adicionar todos os models que podem ser modificados pela pagina admin

admin.site.register(Task)