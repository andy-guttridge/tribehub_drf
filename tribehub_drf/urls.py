"""tribehub_drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.i18n import JavaScriptCatalog
from .views import root_route, logout_route, UsersList

urlpatterns = [
    path('', root_route),
    path('users/', UsersList.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('dj-rest-auth/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('', include('profiles.urls')),
    path('', include('tribes.urls')),
    path('', include('events.urls')),
    path('', include('notifications.urls')),
    path('', include('contacts.urls')),
]

# Config code for recurrence field from
# https://django-recurrence.readthedocs.io/en/latest/installation.html#install
js_info_dict = {
    'packages': ('recurrence', ),
}

urlpatterns += [
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
]
