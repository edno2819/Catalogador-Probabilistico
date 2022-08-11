from django.utils.html import format_html
from django.contrib import admin
from django.db import models
from django.conf import settings


class Tarefa(models.Model):
    status_choices = (("Off", "Off" ), ('On', 'On'))

    nome = models.CharField(max_length=40, primary_key=True)
    status = models.CharField(choices=status_choices, default='Off', max_length=32, null=True, blank=True)
    data = models.DateTimeField(null=True, blank=True)
    ultima_execucao = models.DateTimeField(null=True, blank=True)
    execucao = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.nome

    @admin.display(ordering='Ativar')
    def runTask(self):
        run = format_html(
            '''<button 
            style="background-color: #319c35; border:#319c35 ;color: rgb(255, 255, 255); border-radius: 5px;"
            >
            <a style="color: rgb(255, 255, 255)" href="{}/task/{}">Run<a/>
            </button>''', 
            settings.DEFAULT_DOMAIN,
            self.nome,
        )  

        off = format_html(
            '''''<button 
            style="background-color: #a71c1c; border:#a71c1c ;color: rgb(255, 255, 255); border-radius: 5px;">
            <a >Off<a/>
            </button>''', 
            self.nome,
        )  

        return run if self.status=='Off' else off

    @admin.display(ordering='Ativar')
    def Status_Tarefa(self):
        color = 'a71c1c' if self.status=='Off' else '319c35'
        return format_html(
            '''<button 
            style="background-color: #{}; border:#{} ;color: rgb(255, 255, 255); border-radius: 5px;"
            >{}</button>''',
            color,
            color,
            self.status,
        ) 

    @admin.display(ordering='Ativar')
    def Ultima_atualização(self):
        return self.data

