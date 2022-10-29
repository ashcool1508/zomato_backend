from .models import *
from rest_framework import serializers


class RedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest
        fields = "__all__"


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"
