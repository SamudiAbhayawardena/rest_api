from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializer import UserDetailsSerializer
from rest_framework.response import Response
from accounts.models import User
from .models import UserDetails
from notifications.serializer import NotificationSerializer


class UserDetailsView(GenericAPIView):
    serializer_class = UserDetailsSerializer
    notification_serializer = NotificationSerializer
    def post(self, request):
        filter_data = User.objects.filter(email=request.data.get('email'))

        if filter_data.exists():
            request.data['user_res'] = filter_data.first().id
            user_details = request.data
            serializer = self.serializer_class(data=user_details)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user_data = serializer.data

                notification = {'user_res' : filter_data.first().id, 'notification' : 'Hooray!, Welcome', 'description' : 'welcome to the app.you can check your recomendations and diet plans throgh this app.'}
                notific_Serializer = self.notification_serializer(data=notification)
                if notific_Serializer.is_valid():
                    notific_Serializer.save()

                return Response({'data' : user_data, 'notification' : notific_Serializer.data, 'status' : 'success'}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request):
        ids = User.objects.filter(email=request.data.get('email'))
        
        if ids.exists():
            user_details = UserDetails.objects.get(user_res=ids.first().id)
            serializer = self.serializer_class(user_details, data=request.data, partial=True)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user_data = serializer.data

                notification = {'user_res' : ids.first().id, 'notification' : 'Your Details Updated', 'description' : 'Your personal details updated successfully.'}
                notific_Serializer = self.notification_serializer(data=notification)
                if notific_Serializer.is_valid():
                    notific_Serializer.save()

                return Response({"data" : user_data, "status" : "success", 'notification' : notific_Serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class UserDetailsViewGet(GenericAPIView):
    serializer_class = UserDetailsSerializer

    def post(self, request):
        ids = User.objects.filter(email=request.data.get('email'))

        if ids.exists():
            filter_data = UserDetails.objects.filter(user_res=ids.first().id)
            
            try :
                height_in_meters = filter_data.first().height / 100
                bmi = filter_data.first().weight / (height_in_meters * height_in_meters)

                user = {
                    "name" : filter_data.first().name,
                    "profile" : filter_data.first().profile,
                    "birthday" : filter_data.first().birthday,
                    "gender" : filter_data.first().gender,
                    "height" : filter_data.first().height,
                    "weight" : filter_data.first().weight,
                    "diabetics_score" : filter_data.first().diabetics_score,
                    "bmi" : bmi,
                    "veg_status" : filter_data.first().veg_status
                }
                return Response(user, status=status.HTTP_200_OK)
            
            except :
                return Response({"result" : "not updated"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)
    

