from django.urls import path
from .views import GenerateTopCareers,GenerateUpskilling, GenerateRelatedCareers, GenerateSkillResources

urlpatterns = [
    path('generate-top-careers/', GenerateTopCareers.as_view(), name='GenerateTopCareers'),
    path('generate-upskilling/', GenerateUpskilling.as_view(), name='GenerateUpskilling'),
    path('generate-related-careers/', GenerateRelatedCareers.as_view(), name='GenerateRelatedCareers'),
    path('generate-skill-resources/', GenerateSkillResources.as_view(), name='GenerateSkillResources'),
]
