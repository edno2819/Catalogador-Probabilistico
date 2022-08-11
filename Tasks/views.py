from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.shortcuts import render
from Tasks.models import Tarefa
from Tasks import screduler
import datetime


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)


def tasks_view(request, task_name=''):
    if request.user.__str__()!='AnonymousUser':
        permissions_user = [c for c in get_user_permissions(request.user)]
        if 'Can add tarefa' in str(permissions_user):
            method_to_call = getattr(screduler, task_name)
            method_to_call()
            Tarefa.objects.filter(nome=task_name).update(status='On', data=datetime.datetime.now())
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'base.html') 


