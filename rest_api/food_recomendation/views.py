from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from user_details.models import UserDetails

# data analysis and ml libraries import
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import random

class FoodRecomendationView(GenericAPIView):

    def post(self, requset):
        try:
            # Filter user and user details
            filtered_user = User.objects.filter(email=requset.data.get('email'))
            if not filtered_user.exists():
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            user_details = UserDetails.objects.filter(user_res=filtered_user.first().id)
            if not user_details.exists():
                return Response({"error": "User details not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Get user diabetic score
            diabetics_score = user_details.first().diabetics_score
            # get user non-veg/veg status
            veg_st = user_details.first().veg_status

            # Read dataset
            dataset = pd.read_csv(r"C:\Users\Dell\Desktop\rest_api\rest_api\datasets\foods_details.csv")
            
            # Function to filter vegetarian/non-vegetarian foods
            def filter_veg_status(data, veg_status):
                if veg_status == "veg":
                    return data[data["meal_for"] == "veg"]  # Assuming a "veg" column exists
                elif veg_status == "non-veg":
                    return data[data["meal_for"] == "non-veg"]
                else:
                    return data  # Return all data if veg_status is not specified

            # Filter dataset based on veg_status
            filtered_data = filter_veg_status(dataset.copy(), veg_st)

            # Create diabetic suitability label considering diabetics_score
            filtered_data["diabetic_suitability"] = filtered_data["glycamic_index"].apply(lambda x: 0 if diabetics_score > 100 and x > 45 else 1)
            
            # calculate recomendation precentage by user diabetics level
            filtered_data['precentage'] = filtered_data['glycamic_index'].apply(lambda x: (((diabetics_score - (x * 2))/100) * 100) if diabetics_score > 120 and x < 35 else (diabetics_score - x) / 100 * 100)

            # Select features and split data
            features = ["carbs", "fiber", "sugar", "fat", "protien", "glycamic_index"]
            X_train, X_test, Y_train, Y_test = train_test_split(
                filtered_data[features],
                filtered_data["diabetic_suitability"],
                test_size=0.1,
                random_state=random.randint(1, 200),
                shuffle=True,
            )

            # Train the Random Forest Classifier
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, Y_train)

            # Make predictions and create recommended data
            predicted_labels = model.predict(X_test)
            recommended_data = pd.concat([X_test, pd.DataFrame(predicted_labels, columns=["diabetic_suitability"])], axis=1)

            # adding more data fields to trained data to the trained dataset
            if len(dataset) > len(recommended_data):
                more_data = dataset.sample(len(recommended_data))  # Sample additional data from original dataset
                filtered_data = pd.concat([filtered_data, more_data], ignore_index=True)
                # Repeat training and prediction steps using the expanded filtered_data
            
            final_data = filtered_data[filtered_data['diabetic_suitability'] == 1]
            final_data = final_data.sample(frac=1)
            #convert to json and send response to the client
            json_data = final_data.to_json(orient='records')

            return Response({"diabetics_score": diabetics_score, "recommended_foods": json_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  

class RecommendMealsView(GenericAPIView):

    def post(self, request):
        try:
            user = User.objects.filter(email=request.data.get('email'))
            if user.exists():
                # get user details where store in database related to the email address
                user_details = UserDetails.objects.filter(user_res=user.first().id)
                # read user diabetics score from database
                #user_diabetics_score = user_details.first().diabetics_score
                
                # define diabetics level
                self.diab_level = ""

                # read dataset
                dataset = pd.read_csv(r"C:\Users\Dell\Desktop\rest_api\rest_api\datasets\meal_plans.csv")

                # filter veg, non-veg ststus
                def filter_veg_status(data, status):
                    if status == "veg":
                        return data[data['preference_type'] == "veg"]
                    else :
                        return data
                    
                # filter data by level
                def filter_by_diabetics_level(data, status):
                    if status == "low":
                        return data[data['diabetics_level'] == "low"]
                    elif status == "high":
                        return data[data['diabetics_level'] == "high"]
                    else:
                        return data
                    
                # call filtring methods
                filtered_data1 = filter_veg_status(dataset, user_details.first().veg_status)
                filtterd_data2 = filter_by_diabetics_level(filtered_data1, self.diab_level)

                # define features for training
                features = ["carb", "proteins", "fat", "glycemic_index"]
                target = "diabetics_level"

                #precentage add
                user_diabetics_score = user_details.first().diabetics_score
                filtterd_data2['precentage'] = filtterd_data2['glycemic_index'].apply(lambda x: (((user_diabetics_score - (x * 2))/100) * 100) if user_diabetics_score > 120 and x < 35 else (user_diabetics_score - x) / 100 * 100)
               
                # train test splitting
                X_train, X_test, Y_train, Y_test = train_test_split(filtterd_data2[features], filtterd_data2[target], test_size=0.8)

                # training model
                model = RandomForestClassifier(n_estimators=100, random_state=5)
                model.fit(X=X_train, y=Y_train)

                #predicted_lables = model.predict(X_test)
                #recomend_data = pd.concat([X_test, pd.DataFrame(predicted_lables, columns=["carb"])], axis=1)

                # final data 
                final_data = filtterd_data2.sample(frac=1)

                # convert to json and send to the client
                json_data = final_data.to_json(orient='records')
                return Response({"data" : json_data},status=status.HTTP_200_OK)
        
        # handle errors
        except Exception as e:
            return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)