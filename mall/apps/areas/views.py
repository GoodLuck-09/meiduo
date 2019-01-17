from .serializers import AreaSerializer, SubAreaSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Area
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin, CacheResponseMixin


class AreaModelViewSet(CacheResponseMixin, ReadOnlyModelViewSet):

    # queryset = Area.objects.all()/
    # serializer_class = AreaSerializer
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)

        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer





