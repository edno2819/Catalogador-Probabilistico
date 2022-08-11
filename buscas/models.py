from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from datetime import datetime
from django.contrib import admin
from django.utils.html import format_html




class Paridade(models.Model):
    name = models.CharField(primary_key=True, max_length=10, null=False, blank=False,
    validators=[RegexValidator('^[A-Z_]*$',
                               'Apenas Letras maiúsculas permitidas')])

    def __str__(self):
        return self.name


class Configuração(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=32, null=False, blank=False)
    senha = models.CharField(max_length=32, null=False, blank=False)
    dias_salvos = models.PositiveIntegerField(default=10, null=False, blank=False,
            validators=[
                MaxValueValidator(50),
                MinValueValidator(1)
            ])
    
    class Meta:
        verbose_name_plural = 'configurações'

    def __str__(self):
        return f'Login: {self.login}  | Dias Salvos: {self.dias_salvos}'


class Chance(models.Model):
    direc_choices = (("CALL", "COMPRA" ), ('SELL', 'VENDA'))
    time_choices = ((1, '1'), (5, '5'), (15, '15'))

    par = models.CharField(max_length=32)
    timeframe = models.PositiveSmallIntegerField(choices=time_choices, null=False, blank=False)
    hora = models.PositiveSmallIntegerField(null=False, blank=False)
    minuto = models.PositiveSmallIntegerField(null=False, blank=False)
    call = models.PositiveSmallIntegerField(null=False, blank=False)
    sell = models.PositiveSmallIntegerField(null=False, blank=False)
    porcent = models.PositiveSmallIntegerField(null=False, blank=False)
    direc = models.CharField(max_length=32, choices=direc_choices,  null=False, blank=False)


    class Meta:
        unique_together = (("par", "timeframe", "hora", "minuto"))

    def formatData(self):
        self.horario = datetime.strptime(f'{self.hora}:{self.minuto}', "%H:%M").__str__()[11:16]
        return self.horario

    def __str__(self):
        return f'{self.par}-{self.direc}-{self.porcent}%'
    

class Vela(models.Model):
    direc_choices = (("CALL", "COMPRA" ), ('SELL', 'VENDA'))
    time_choices = ((1, '1'), (5, '5'), (15, '15'))

    par = models.CharField(max_length=32)
    data = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
    timeframe = models.PositiveSmallIntegerField(choices=time_choices, null=False, blank=False)
    hora = models.PositiveSmallIntegerField(null=False, blank=False)
    minuto = models.PositiveSmallIntegerField(null=False, blank=False)
    direc = models.CharField(max_length=32, choices=direc_choices,  null=False, blank=False)

    class Meta:
        unique_together = (("par", "timeframe", "data", "hora", "minuto"),)
        
    @admin.display(boolean=False)
    def Horário(self):
        self.horario = datetime.strptime(f'{self.hora}:{self.minuto}', "%H:%M").__str__()[11:16]
        return self.horario

    @admin.display(ordering='direc')
    def Direção(self):
        color = 'a71c1c' if self.direc=='SELL' else '319c35'
        return format_html(
            '''<button 
            style="background-color: #{}; border:#{} ;color: rgb(255, 255, 255); border-radius: 5px;"
            href = 'http://127.0.0.1:8000/admin/buscas/chance/
            >{}</button>''',
            color,
            color,
            self.direc,
        )  

    def __str__(self):
        return f'{self.data}-{self.par}-{self.timeframe}-{self.direc}'


#========================================== functions =======================================================================

def analyVelas(par, timeframe, hora, minuto, limit=10):
    datas = Vela.objects.filter(par=par, timeframe=timeframe, hora=hora, minuto=minuto).order_by('-data')[:limit]

    if len(datas)<limit:
        return False, False, False, False

    result = {'CALL':0, 'SELL':0}
    for data in datas:
        if data.direc=='CALL':
            result['CALL'] += 1
        else:
            result['SELL'] += 1

    if result['CALL']==0 and result['CALL']==0:
        return False, False, False, False
    
    direc, maxi = ('CALL', result['CALL']) if result['CALL']>result['SELL']  else ('SELL', result['SELL'])  
    taxa = int((100*maxi)/(result['CALL']+result['SELL']))
    return direc, result['CALL'], result['SELL'], taxa
