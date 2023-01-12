from django.urls import path
from contacts import views

urlpatterns = [
    path('contacts/', views.ContactListCreate.as_view()),
    path('contacts/<int:pk>/', views.ContactDetail.as_view()),
]
