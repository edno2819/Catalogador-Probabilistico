from buscas.models import Paridade, Configuração, Chance, Vela
from django.contrib import admin


class VelasAdmin(admin.ModelAdmin):
    fields = (('par', 'timeframe'), 'data', 'direc')
    list_display = ('data', 'par', 'Horário', 'Direção')
    search_fields = ['minuto']
    list_filter = ('par', 'data', 'timeframe', 'hora')

    search_help_text = 'Par Timeframe Hora Minuto'
    sortable_by = ['direc']

    @admin.display(ordering='data')
    def dia(self, obj):
        return obj.data.first_name



def ação_personalizada(modeladmin, request, queryset):
    for scenario in queryset:
        #Do something
        pass

class ChancesAdmin(admin.ModelAdmin):
    list_display = ('timeframe', 'par', 'hora', 'minuto', 'direc')
    search_fields = ['minuto']
    list_filter = ('par', 'timeframe', 'hora')
    actions = [ação_personalizada]

    sortable_by = ['direc']

class ConfigsAdmin(admin.ModelAdmin):
    fields = ('login', 'senha', 'dias_salvos')





admin.site.register(Paridade)
admin.site.register(Configuração, ConfigsAdmin)
admin.site.register(Chance, ChancesAdmin)
admin.site.register(Vela, VelasAdmin)
