from django.urls import path
from . import views


urlpatterns = [
    path('', views.PredictView.as_view(), name='predict'),
]