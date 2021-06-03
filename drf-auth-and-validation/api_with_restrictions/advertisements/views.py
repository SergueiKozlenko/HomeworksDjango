from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorites
from advertisements.serializers import AdvertisementSerializer, FavoritesSerializer
from rest_framework import status
from rest_framework.response import Response


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.is_staff


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            permissions = [IsAuthenticated]
        elif self.action in ["destroy", "update", "partial_update"]:
            permissions = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permissions = []
        return [permission() for permission in permissions]

    def get_queryset(self):
        queryset = Advertisement.objects.filter(status__in=["OPEN", "CLOSED"])
        if self.request.user.is_authenticated:
            draft = Advertisement.objects.filter(status="DRAFT", creator=self.request.user)
            return queryset | draft
        return queryset


class FavoritesViewSet(ModelViewSet):
    """ViewSet для избранного."""

    serializer_class = FavoritesSerializer
    filter_backends = [DjangoFilterBackend]

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(Favorites.objects.filter(user=self.request.user))
        return Favorites.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = Favorites.objects.get(user=request.user, advertisement_id=kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
