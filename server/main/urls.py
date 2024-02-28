from django.urls import path
from .views import GenerateTopCareers,GenerateUpskilling

urlpatterns = [
    path('generate-top-careers/', GenerateTopCareers.as_view(), name='GenerateTopCareers'),
    path('generate-upskilling/', GenerateUpskilling.as_view(), name='GenerateUpskilling'),
]
