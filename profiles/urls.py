from django.urls import path
from profiles import views

urlpatterns = [
    path('accounts/tribe', views.TribeAccount.as_view()),
    path('accounts/user', views.UserAccount.as_view()),
    path('accounts/user/<int:pk>', views.DeleteUser.as_view()),
    path('profile/<int:pk>', views.ProfileDetail.as_view()),
]
