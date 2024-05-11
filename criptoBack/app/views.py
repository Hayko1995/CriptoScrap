from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import *
from .serializers import *
# Create your views here.


class getCoins(APIView):

    def post(self, request, *args, **kwargs):

        try:
            serializer = CoinsSerializer(
                Coins.objects.all(), many=True)
            print(serializer.data)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            return response

        except:

            return Response(status=status.HTTP_404_NOT_FOUND)
