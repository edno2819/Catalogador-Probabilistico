from django.contrib import admin
from django.urls import path
from buscas import views
from Tasks.views import tasks_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.busca, name='busca'),
    path('resultado', views.busca, name='busca'),
    path('task/<task_name>', tasks_view),
]
