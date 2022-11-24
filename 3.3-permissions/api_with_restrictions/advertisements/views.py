from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrAdmin


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    def get_queryset(self):
        user = self.request.user.id
        queryset = Advertisement.objects.exclude(Q(status='DRAFT') & ~Q(creator=user))
        return queryset

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action in ['add_into_favourites', 'remove_from_favourites', 'favourites']:
            return [IsAuthenticated()]
        return []

    @action(detail=False, permission_classes=[IsAuthenticated])
    def favourites(self, request):
        """Избранное"""
        queryset = Advertisement.objects.filter(all_favourites=request.user)
        serializer = AdvertisementSerializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_into_favourites(self, request):
        """Добавление в избранное"""
        user = request.user
        advertisement = Advertisement.objects.get(id=request.data["id"])

        if advertisement in user.favourites.all():
            return Response('Объявление уже в избранном')
        elif advertisement.creator == user:
            return Response('Вы не можете добавить в избранное своё объявление')
        elif advertisement.status != 'OPEN':
            return Response('В избранное можно добавить только открытые объявления')
        user.favourites.add(advertisement)

        return Response('Объявление добавлено в избранное')

    @action(detail=False, methods=['delete'])
    def remove_from_favourites(self, request):
        """удаление из избранного"""
        user = request.user
        advertisement = Advertisement.objects.get(id=request.data["id"])

        if advertisement not in user.favourites.all():
            return Response('Объявление не в избранном')
        user.favourites.remove(advertisement)

        return Response('Объявление удалено из избранного')
