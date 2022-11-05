import numpy as np
import pandas as pd
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import *
from .recommendation import foodrecommendation
from .serializers import *



class AllRes(APIView):
    def get(self, request):
        try:
            activity_data = Rest.objects.all()
            serializer = RedSerializer(activity_data, many=True)
            return JsonResponse({"response": serializer.data}, status=200)
        except Exception as e:
                print(e)
                return JsonResponse({"response": False}, status=400)

class ResfoodItemsList(APIView):
    def get(self, request):
        try:
            res_id = request.query_params['res_id']
            activity_data = FoodItem.objects.filter(res_menu_id=res_id)
            serializer = FoodSerializer(activity_data, many=True)
            return JsonResponse({"response": serializer.data}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"response": False}, status=400)
class OrderUser(APIView):
    def post(self, request):
        try:
            user_id = request.data['user_id']
            res_id = request.data['res_id']
            food_id = request.data['food_id']
            user = NewUser.objects.get(id=user_id)
            order = Order_placed(userdetail=user,resdet=res_id,fooddet=food_id)
            order.save()
            # df = pd.read_csv("new_reviews.csv")
            # new_df = df[["ProductId", "UserId", "Score"]]
            # found = False
            # for ind in new_df.index:
            #     if new_df['ProductId'][ind] == food_id and new_df['UserId'][ind] == user_id:
            #          new_df['Score'][ind] += 1
            #          found = True
            # if not found:
            #     new_row = {'ProductId': food_id, 'UserId': user_id, 'Score': 1}
            #     new_df = new_df.append(new_row, ignore_index=True)
            # global emb_user, emb_food, user_ids, food_ids
            # emb_user, emb_food, user_ids, food_ids = foodrecommendation()

            return JsonResponse({"response": True}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"response": False}, status=400)

def get_recommandation(user_id,emb_user,emb_food,user_ids,food_ids, num_recommadations):
    ratings_predicted = np.matmul(np.reshape(emb_user[user_ids[list(user_ids.keys())
    [list(user_ids.values()).index(user_id)]]], (1, 5)), np.transpose(emb_food))
    recommanded_index = ratings_predicted[0].argsort()[-num_recommadations:][::-1]
    for i in range(5):
        recommanded_index[i] = food_ids[recommanded_index[i]]
    return recommanded_index

# def get_recommandation(user_id, emb_user, emb_food, num_recommadations):
#       ratings_predicted = np.matmul(np.reshape(emb_user[user_ids[list(user_ids.keys())
#           [list(user_ids.values()).index(user_id)]]], (1, 5)), np.transpose(emb_food))
#       recommanded_index = ratings_predicted[0].argsort()[-num_recommadations:][::-1]
#       for i in range(5):
#         recommanded_index[i] = food_ids[recommanded_index[i]]
#       return recommanded_index
#
#     for i in range(5):
#       print(get_recommandation(i, emb_user, emb_food, 10))
class GetRecommendation(APIView):

    def post(self, request):
        try:
            user_id = request.data['user_id']
            emb_user, emb_food, user_ids, food_ids = foodrecommendation()
            recommended = get_recommandation(user_id=int(user_id),emb_user=emb_user,emb_food=emb_food,user_ids=user_ids,
                                             food_ids=food_ids ,num_recommadations=5)
            print(type(recommended))

            # foodrecommendation()
            foodslist = []
            for i in recommended:
                food_id = str(i)
                print(type(food_id))
                food = FoodItem.objects.filter(food_id=food_id)
                serializer = FoodSerializer(food, many=True)
                foodslist.append(serializer.data)
            print(foodslist)
            return JsonResponse({"response": True}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"response": False}, status=400)

class LoginView(APIView):
    def get(self, request):
        email = request.query_params['email']
        print(email)
        otp = int(request.query_params['otp'])
        print(otp)
        user = authenticate(email= email, password = otp)
        if user is not None:
            user_object = NewUser.objects.get(email=email)
            print(user_object)
            user_id = user_object.id
            user_email = user_object.email
            data = {
                'id':user_id,
                'email':user_email,
                'username':user.username,
            }
            return JsonResponse({"message":"verified", "user":data}, status=200)
        else:
            return JsonResponse({"message":"incorrect otp"}, status=200)
    def post(self, request):
        email = request.data['email']
        username = request.data['username']
        # def sendotpfinal(email):
        #     otp = int((random.uniform(0, 1))*100000)
        #     # print(otp)
        #     if otp <= 100000 and otp >10000:
        #         otp = f"{otp}"
        #     elif otp <= 10000 and otp >1000:
        #         otp = f"0{otp}"
        #     elif otp <= 1000 and otp >100:
        #         otp = f"00{otp}"
        #     elif otp <= 100 and otp >10:
        #         otp = f"000{otp}"
        #     elif otp <= 10 and otp >1:
        #         otp = f"0000{otp}"
        #     otp = str(otp)
        #     # print(otp)
        #     sendotp(email,otp)
        #     changepassword(email, otp)
        #     return "OTP Sent"
        # foo = sendotpfinal(email)
        try:
            user = NewUser.objects.get(email=email)
            data = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
            return JsonResponse(data, status=200)
        except Exception as e:
            user_object = NewUser(email=email,username=username)
            user_object.save()
            print(user_object)
            user_email = user_object.email
            data = {
                "id": user_object.id,
                "email": user_email,
                "username":user_object.username
            }
            return JsonResponse(data, status=200)
def sendotp(email, otp):
    message = Mail(
            from_email="noreply@ripik.in",
            to_emails=email,
            subject='OTP for logging In',
            html_content=f'Your OTP for logging in is {otp}. Thank you for using our services.',
        )
    sendgrid_client = SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)
    response = sendgrid_client.send(message=message)
    print(response.status_code)
    # subject = 'OTP for logging In'
    # message = f'Your OTP for logging in is {otp}. Thank you for using our services.'
    # email_from = 'noreply@ripik.in'
    # recipient_list = [email]
    # # print("email sent")
    # send_mail( subject, message, email_from, recipient_list, fail_silently=False, )

    

def changepassword(email,otp):
    user = NewUser.objects.all().filter(email = email).first()
    if user:
        user.set_password(otp)
        user.save()
        # print(otp)
    else: 
        user = NewUser.objects.create_user(email=email, password=otp)
        print(otp)
        user.save()
    # print("passwordchanged")
    # print(user)
