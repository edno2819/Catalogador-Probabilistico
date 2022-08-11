from buscas.models import Paridade, Chance
from django.shortcuts import render
from datetime import timedelta



def home(request):
    context = {'pares':Paridade.objects.filter()}
    return render(request, 'index.html', context)


def layout(request):
    return render(request, 'teste.html') 


def format_chance(datas):
    limit = 500
    chances = []
    for chance in datas[:limit]:
        horario = (timedelta(hours=chance.hora, minutes=chance.minuto) + timedelta(minutes=chance.timeframe)).seconds
        after_hora = horario//3600
        after_minuto = int((horario%3600)/60)
        vela_anterior = Chance.objects.filter(par=chance.par, timeframe=chance.timeframe, hora=after_hora, minuto=after_minuto)
        new = {'horario':chance.formatData(), 'par':chance.par, 'porcent':chance.porcent, 'timeframe':chance.timeframe, 'direc':chance.direc}
        if len(vela_anterior)==1:
            vela_anterior = vela_anterior[0]
            new.update({'horario_after':vela_anterior.formatData(), 'porcent_after':vela_anterior.porcent, 'direc_after':vela_anterior.direc})
        chances.append(new)
    return chances


def busca(request):
# '__lt' ou menor ou igual '__lte' (< <=) and gt get
    datas = Chance.objects.all().order_by('-porcent','-par')

    chances = format_chance(datas)

    context = {'pares':Paridade.objects.filter(), 'resultado_qtd':len(datas), 'chances':chances}

    if request.method == "POST":
        par = request.POST.get('par', False)

        time = int(request.POST.get('time', False))

        hora = request.POST.get('hora', False)
        hora = int(hora) if hora!='' else False

        minuto = request.POST.get('minuto', False)
        minuto = int(minuto) if minuto!='' else False

        main_taxa = request.POST.get('main_taxa', False)
        main_taxa = int(main_taxa) if main_taxa!='' else False

        second_taxa = request.POST.get('second_taxa', False)
        second_taxa = int(second_taxa) if second_taxa!='' else False



        datas = Chance.objects.filter(par=par) if par else Chance.objects.all() 
        datas = datas.filter(hora=hora) if hora else datas
        datas = datas.filter(minuto=minuto) if minuto else datas
        datas = datas.filter(porcent__gte=main_taxa) if main_taxa else datas
        datas = datas.filter(timeframe=time) if time else datas
        datas = datas.order_by('-porcent','-par')

        chances = format_chance(datas)

        if type(second_taxa)==int:
            new_chance = []
            for chance in chances:
                if 'porcent_after' in chance.keys() and chance['porcent_after']>=second_taxa:
                    new_chance.append(chance)
        else:
            new_chance = chances

        context.update({'chances': new_chance, 'resultado_qtd':len(new_chance)})
        return render(request, 'result.html', context) 

    return render(request, 'result.html', context) 

