from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.contrib.auth import authenticate
from .serializer import UserSerializer, LoginSerielizer
from rest_framework.response import Response
from user_details.models import UserDetails
from .models import User
from notifications.serializer import NotificationSerializer
#from .utils import send_mail


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user_details = request.data
        serializer = self.serializer_class(data=user_details)

        #check data valid or not
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            #send_mail(user['email'])
            return Response({'data' : user, 'status' : 'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerielizer
    notification_serializer = NotificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request' : request})
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=request.data.get('email'))
        if user.exists():
            user_details = UserDetails.objects.filter(user_res=user.first().id)
            if user_details.exists():
                notification = {'user_res' : user.first().id, 'notification' : 'Successfully Logged in', 'description' : 'You successfully logged in to the system.check your recomendations.'}
                notific_Serializer = self.notification_serializer(data=notification)

                if notific_Serializer.is_valid():
                    notific_Serializer.save()
                else:
                    pass

                data = {
                    'security' : serializer.data,
                    'name' : user_details.first().name,
                    'profile' : user_details.first().profile,
                    'birthday' : user_details.first().gender,
                    'height' : user_details.first().height,
                    'weight' : user_details.first().weight,
                    'diabetics_score' : user_details.first().diabetics_score,
                    'bmi' : user_details.first().weight / (user_details.first().height * user_details.first().height),
                    'notification' : notific_Serializer.data,
                }

                return Response(data, status=status.HTTP_200_OK)
            
            return Response({"security" : serializer.data},status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class DeleteUserView(GenericAPIView):
    serializer_class = LoginSerielizer

    def post(self, request):
        try:
            if not request.data.get('email') or not request.data.get('password'):
                return Response({'result' : 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, email=request.data.get('email'), password=request.data.get('password'))
            if user is None:
                return Response({'result': 'invalid data'}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.delete()
            return Response({'result' : 'success'}, status=status.HTTP_200_OK)
        
        except Exception as e :
            return Response({'result' : 'user not found', 'reason' : str(e)}, status=status.HTTP_404_NOT_FOUND)
            