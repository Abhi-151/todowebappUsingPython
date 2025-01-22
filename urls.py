from django.urls import path
from . import views

urlpatterns = [
    path('get_tasks', views.get_tasks),
    path('create_task', views.create_task),
    path('bulk_create_tasks', views.bulk_create_tasks),
    # path('update_task', views.update_task),
    path('update_tasks', views.update_tasks),
    path('admin_login', views.admin_login),
    path('create_admin', views.create_admin),
]
