from django import urls
from core import views

app_name = 'core'

urlpatterns = [
    urls.path('login', views.LoginView.as_view(), name='login'),
    urls.path('logout', views.LogoutView.as_view(), name='logout'),
    urls.path('', views.IndexView.as_view(), name='index'),
]
