from django.urls import path
from . import views

urlpatterns = [
    path("", views.base),
    path("ping/", views.ping),
    path('reading/training-levels/', views.training_levels, name='training_levels'),
]