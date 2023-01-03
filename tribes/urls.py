from django.urls import path
from tribes import views

urlpatterns = [
    path('tribe/', views.TribeList.as_view()),
]
