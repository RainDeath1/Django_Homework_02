from rest_framework import serializers
from .models import AdvUser, Character
from django.utils.translation import gettext_lazy as _


class AdvUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label=_("Подтверждение пароля"))

    class Meta:
        model = AdvUser
        fields = ('id', 'username', 'password', 'password2', 'email', 'bio', 'avatar',
                  'favorite_race', 'favorite_class', 'experience_level', 'is_dm')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError(_("Пароли должны совпадать."))
        return data

    def create(self, validated_data):
        user = AdvUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=validated_data.get('bio', ''),
            avatar=validated_data.get('avatar'),
            favorite_race=validated_data.get('favorite_race', ''),
            favorite_class=validated_data.get('favorite_class', ''),
            experience_level=validated_data.get('experience_level', 'beginner'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            'id', 'name', 'character_class', 'race', 'level', 'image',
            'strength', 'dexterity', 'constitution', 'intelligence',
            'wisdom', 'charisma', 'strength_modifier', 'dexterity_modifier',
            'constitution_modifier', 'intelligence_modifier', 'wisdom_modifier',
            'charisma_modifier', 'armor_class'
        ]
