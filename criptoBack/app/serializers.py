from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta():
        model = Product
        fields = "__all__"


class CoinsSerializer(serializers.ModelSerializer):
    class Meta():
        model = Coins
        fields = "__all__"


