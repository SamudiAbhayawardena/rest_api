from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializer import HealthHistorySerializer
from rest_framework.response import Response
from accounts.models import User
from .models import HealthHistory

# Create your views here.
class HistoryView(GenericAPIView):
    serializer_class = HealthHistorySerializer

    def post(self, request):
        filter_data = User.objects.filter(email=request.data.get('email'))

        if filter_data.exists():
            request.data['user'] = filter_data.first().id
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = serializer.data

                return Response({'data' : data, 'status' : 'success'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class HistoryViewGet(GenericAPIView):
    serializer_class = HealthHistorySerializer

    def post(self, request):
        filter_data = User.objects.filter(email=request.data.get('email'))

        if filter_data.exists():
            data = HealthHistory.objects.filter(user=filter_data.first().id)
            json_data = serialize('json', data.all())
            return Response({"data" : json_data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)