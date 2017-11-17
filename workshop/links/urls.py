from django.conf.urls import url, include
from django.views import generic
from rest_framework import routers

from . import views
from .api import LinkTagViewSet, LinkViewSet, TagViewSet, UserViewSet


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'links', LinkViewSet)
router.register(r'tags', TagViewSet)
router.register(r'linktags', LinkTagViewSet)


urlpatterns = [
    url(r'^view2/',
        generic.TemplateView.as_view(template_name='view2.html')),
    url(r'^$', views.links_detail),
    url(r'^api/', include(router.urls)),
]
