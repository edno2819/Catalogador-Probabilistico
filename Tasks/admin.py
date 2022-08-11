from django.contrib import admin
from Tasks.models import Tarefa


class TarefaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'Status_Tarefa', 'data', 'ultima_execucao', 'execucao', 'runTask')
    fields = ('nome', 'status')



admin.site.register(Tarefa, TarefaAdmin)