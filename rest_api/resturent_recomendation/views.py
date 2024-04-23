from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from user_details.models import UserDetails
import pandas as pd

class ResturentRecomendationView(GenericAPIView):

    def post(self, request):
        dataset = pd.read_csv(r'C:\Users\Dell\Desktop\rest_api\rest_api\datasets\resturents.csv')

        try:
            city = request.data['city'].lower()

            dataset = dataset.drop_duplicates()

            dataset['average_rating'] = (dataset['rate'] * dataset['reviews'] / dataset['reviews'])
            data = dataset.sort_values(by=['average_rating'], ascending=False)
            reviewd_data = data.groupby(['reviews']).apply(pd.DataFrame.sample).reset_index(drop=True)

            reviewd_data = reviewd_data.reset_index(drop=True)
            reviewd_data = reviewd_data[reviewd_data['city'] == city].sample(frac=1).head(3)
            
            datas = reviewd_data[['id','name', 'city', 'contact', 'rate', 'short_desc', 'long_desc', 'latitude', 'longtiude', 'reviews', 'image', 'image2', 'image3', 'image4', 'image5']]
            json_data = datas.to_json(orient='records')

            return Response(data=json_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status" : "not found", "err" : str(e)}, status=status.HTTP_404_NOT_FOUND)