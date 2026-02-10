from django.urls import path
from . import views  # This line is what was missing!

urlpatterns = [
    path("", views.base),
    path("ping/", views.ping),
    path("wordcard/", views.WordCardView.as_view(), name="wordcard"),
]