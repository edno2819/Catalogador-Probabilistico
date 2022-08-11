from apscheduler.schedulers.background import BackgroundScheduler
from Tasks.wrapperFunctions import Decorators
import backports.zoneinfo as zoneinfo
from django.utils import timezone 
from Tasks.models import Tarefa
import inspect


from buscas import cron



BR = zoneinfo.ZoneInfo("America/Sao_Paulo")

@Decorators.task_run_now_theread
def extract_Reset():
    print(f'Executando Extração completa')
    try:
        cron.ResetValues()
    except Exception as e:
         print(f'Erro: {e}')
    Tarefa.objects.filter(nome=inspect.stack()[0][3]).update(status='Off', data=timezone.now())


@Decorators.task_run_now_theread
def create_chance_1():
    print(f'Executando criação de Chances 1')
    cron.all_dairly_task_half_one(['1'])


@Decorators.task_run_now_theread
def create_chance_5():
    print(f'Executando criação de Chances 5')
    cron.sumDirectionsDjango(['5'])


@Decorators.task_run_now_theread
def create_chance_15():
    print(f'Executando criação de Chances 15')
    cron.sumDirectionsDjango(['15'])

@Decorators.task_run_now_theread
def create_chance_all():
    print(f'Executando criação de Chances all')
    cron.sumDirectionsDjango()


def extracts_1_5_15_2():
    function_name = inspect.stack()[0][3]
    new_func = Decorators.taskWrapper(cron.all_dairly_task_half_two, function_name)

    scheduler = BackgroundScheduler(timezone=BR)
    scheduler.add_job(new_func, 'cron', day_of_week='1,2,3,4,5', hour=0, minute=1)
    scheduler.start()


def extracts_1_5_15_1():
    function_name = inspect.stack()[0][3]
    new_func = Decorators.taskWrapper(cron.all_dairly_task_half_one, function_name)

    scheduler = BackgroundScheduler(timezone=BR)
    scheduler.add_job(new_func, 'cron', day_of_week='0,1,2,3,4', hour=15, minute=51)
    scheduler.start()

