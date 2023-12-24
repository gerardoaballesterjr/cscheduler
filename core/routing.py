from django.urls import re_path 
from core import consumers

urlpatterns = [
    re_path(r'semester/generate/(?P<slug>\w+)', consumers.SemesterConsumer.as_asgi())
]