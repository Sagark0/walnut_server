from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('getMails/', views.getMails),
    path('fetchMails/', views.fetchMails),
    path('updateCategory', views.updateCategory)
]
