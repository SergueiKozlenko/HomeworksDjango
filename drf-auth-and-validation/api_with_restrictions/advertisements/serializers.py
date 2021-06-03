from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, Favorites


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context["request"].user
        users_adv_count = Advertisement.objects.select_related('creator').filter(creator=user, status='OPEN').count()

        if users_adv_count > 10:
            raise serializers.ValidationError('Превышено количество открытых объявлений (10)')

        return data


class FavoritesSerializer(serializers.ModelSerializer):
    """Serializer для избранного."""

    class Meta:
        model = Favorites
        fields = ('advertisement',)

    def validate(self, attrs):
        user = self.context['request'].user
        advertisement = attrs['advertisement']
        creator = attrs['advertisement'].creator
        advertisement_in_favorites = Favorites.objects.filter(user=user) \
            .filter(advertisement=attrs['advertisement'])

        if advertisement.status == 'DRAFT':
            raise ValidationError({'error': 'Черновик нельзя добавлять в избранное'})

        if advertisement_in_favorites.exists():
            raise ValidationError({'error': 'Объявление уже есть в избранном'})

        if user == creator:
            raise ValidationError({'error': 'Собственное объявление нельзя добавлять в избранное'})

        return attrs

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)
