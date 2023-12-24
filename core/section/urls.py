from django import urls
from core.section import views

app_name = 'section'

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name='index'),
    urls.path('create', views.CreateView.as_view(), name='create'),
    urls.path('update/<slug:slug>', views.UpdateView.as_view(), name='update'),
    urls.path('delete/<slug:slug>', views.DeleteView.as_view(), name='delete'),
    urls.path('schedule/<slug:slug>', views.ScheduleView.as_view(), name='schedule'),
]
