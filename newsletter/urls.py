from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='newsletter_index'),
]

