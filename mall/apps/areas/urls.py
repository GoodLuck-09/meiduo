from django.conf.urls import url
from .views import AreaModelViewSet


urlpatterns = [

]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'infos', AreaModelViewSet, base_name='area')

urlpatterns += router.urls
