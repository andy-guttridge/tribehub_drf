from django.urls import path
from profiles import views

urlpatterns = [
    path('register_new_tribe/', views.RegisterNewTribe.as_view()),
    # path('register_new_user/', views.RegisterNewUser.as_view())
]
