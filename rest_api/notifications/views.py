from django.core.serializers import serialize
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from .models import Notifications
from .serializer import NotificationSerializer

class NotificationsSetView(GenericAPIView):
    serializer_class = NotificationSerializer


    def post(self, requset):
        user_obj = User.objects.filter(email=requset.data.get('email'))

        if user_obj.exists():
            requset.data['user_res'] = user_obj.first().id 
            
            serializer = self.serializer_class(data=requset.data)
            if serializer.is_valid():
                serializer.save()

                return Response({'result' : 'success', 'data' : serializer.data}, status=status.HTTP_200_OK)
            return Response({'result' : 'invalid data'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'result' : 'user not found'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):

        notification = Notifications.objects.get(pk=request.data.get('id'))

        try :
            notification.status = True
            notification.save()

            return Response({'data' : "success"}, status=status.HTTP_200_OK)
        except Notifications.DoesNotExist:
            return Response({'result' : 'not found'}, status=status.HTTP_204_NO_CONTENT)
    

class NotificationsGetView(GenericAPIView):

    def post(self, request):
        user_obj = User.objects.filter(email=request.data.get('email'))

        if user_obj.exists():
            notifications = Notifications.objects.filter(user_res=user_obj.first().id)

            json_data = serialize('json', notifications.all())

            return Response({'data' : json_data}, status=status.HTTP_200_OK)
        return Response({'result' : 'user not found'}, status=status.HTTP_204_NO_CONTENT)