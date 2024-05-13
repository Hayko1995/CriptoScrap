from rest_framework import serializers
from .models import *


class CoinsSerializer(serializers.ModelSerializer):
    class Meta():
        model = Coins
        fields = "__all__"


