from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="lm-home"),
    path('perplex/', views.Perplex, name="lm-perplex"),
    path('word/', views.Word, name="lm-word"),
]
