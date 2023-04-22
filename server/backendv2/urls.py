from django.urls import path
from . import views

urlpatterns = [
    path('api/clearall', views.clear_all),
    path('api/create', views.create),
    path('api/read', views.read),
    path('api/update', views.update),
    path('api/delete', views.delete),
    path('api/optimize', views.optimize),
]
