
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import backports.zoneinfo as zoneinfo
from django.utils import timezone 
from Tasks.models import Tarefa
import threading

BR = zoneinfo.ZoneInfo("America/Sao_Paulo")


class Decorators:
    def task_run_now_back(func):
        def wrapper():
            scheduler = BackgroundScheduler(timezone=BR)
            now = datetime.today() + timedelta(seconds=30)
            tomorow = now + timedelta(days=1)
            scheduler.add_job(func, 'cron', hour=now.hour, minute=now.minute, day=now.day, year=now.year, end_date=tomorow.__str__()[:10]+' 00:00:00.000000')
            scheduler.start()

        return wrapper

    def task_run_now_theread(func):
        def wrapper():
            threading.Thread(target=func).start()
        return wrapper

    def taskWrapper(func, function_name):
        def function_return():
            print(f'\n==================={function_name}===================')
            try:
                func()
                Tarefa.objects.filter(nome=function_name).update(ultima_execucao=timezone.now(), execucao='Sucesso' )
            except Exception as e:
                print(f'Erro: {e}')
                Tarefa.objects.filter(nome=function_name).update(ultima_execucao=timezone.now(), execucao='Falha' )
            finally:
                print(f'==================={function_name}===================')

        return function_return

