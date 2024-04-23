from django.core.serializers import serialize
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from user_details.models import UserDetails
from .serializer import CommentSerializer
from .models import Comments


class CommentHistorySetView(GenericAPIView):
    serializer_class = CommentSerializer

    def post(self, request):
        filter_data = User.objects.filter(email=request.data.get('email'))
        if filter_data.exists():
            user_details = UserDetails.objects.filter(user_res=filter_data.first().id)
            if user_details.exists():
                request.data['user_name'] = user_details.first().name
                
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    data = serializer.data

                    return Response({'result' : 'success', 'data' : data}, status=status.HTTP_201_CREATED)
                return Response({'result' : 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            request.data['user_name'] = filter_data.first().email
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = serializer.data

                return Response({'result' : 'success', 'data' : data}, status=status.HTTP_201_CREATED)
            return Response({'result' : 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'result' : 'user details not found'}, status=status.HTTP_404_NOT_FOUND)
    
class CommentHistoryGetView(GenericAPIView):

    def post(self, request):
        fileter_data = Comments.objects.filter(hotel_id=request.data.get('hotel_id'))

        if fileter_data.exists():
            json_convert = serialize('json', fileter_data.all())

            return Response({"result" : "success", "data" : json_convert}, status=status.HTTP_200_OK)
        return Response({"result" : "not found"}, status=status.HTTP_204_NO_CONTENT)