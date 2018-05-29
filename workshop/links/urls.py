from django.urls import path
from django.views import generic

urlpatterns = [
    path('view2/',
        generic.TemplateView.as_view(template_name='view2.html')),
    path('',
        generic.TemplateView.as_view(template_name='view1.html')),
]
