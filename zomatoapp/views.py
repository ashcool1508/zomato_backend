import pandas as pd
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.views import APIView
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import *
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
# class ActivityForUser(APIView):
#     def get(self, request):
#         try:
#             user_id = request.query_params['user_id']
#             activity_data = Activity.objects.filter(user=user_id)
#             serializer = ActivitySerializer(activity_data, many=True)
#             return JsonResponse({"response": serializer.data}, status=200)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"response": False}, status=400)
#
# class Tags(APIView):
#     def post(self, request):
#         try:
#             file = request.FILES['file']
#             df = pd.read_excel(file)
#             sensorandtags = list(zip(df['Sensor'].fillna(""), df['TAG'].fillna("")))
#             return JsonResponse({"response": sensorandtags}, status=200)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"response": False}, status=400)
#
# class AlertData(APIView):
#     def get(self, request):
#         try:
#             user_id = request.query_params['id']
#             alert_data = Alert.objects.filter(user = user_id)
#             # alert_data = Alert.objects.all()
#             serializer = AlertSerializer(alert_data, many=True)
#             return JsonResponse({"response": serializer.data}, status=200)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"response": False}, status=400)
#     def post(self, request):
#         try:
#             equipment_name = request.data['equipment_name']
#             timestamp = request.data['timestamp']
#             location = request.data['location']
#             description = request.data['description']
#             resource = request.data['resource']
#             resource_manager = request.data['resource_manager']
#             area_in_charge = request.data['areaInCharge']
#             aLert_data = Alert(equipment_name=equipment_name, timestamp=timestamp, location=location, description=description,
#                                resource=resource, resource_manager=resource_manager, area_in_charge=area_in_charge)
#             aLert_data.save()
#             return JsonResponse({"response": True}, status=200)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"response": False}, status=400)
#
#
# class EquipmentData(APIView):
#     def get(self, request):
#         try:
#             user_id = request.query_params['id']
#             equipment_Data = Equipment.objects.filter(user=user_id)
#             # equipment_Data = Equipment.objects.all()
#             serializer = EquipmentSerializer(equipment_Data, many=True)
#             return JsonResponse({"equipment_detail": serializer.data}, status=200)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"response":False}, status=400)
#
#     def post(self, request):
#         try:
#             equipment_name = request.data['equipment_name']
#             file = request.FILES['file']
#             tags = request.data['tags']
#             tags_to_string = " ".join(tags)
#             user_tags_data = UserTags(tags=tags_to_string)
#             user_tags_data.save()
#             threshold = 1
#             risk_signal = 1
#             location = "pyro"
#             equipment_data = Equipment(equipment_name=equipment_name, threshold=threshold, risk_signal=risk_signal,location=location)
#             equipment_data.save()
#             return JsonResponse({"response": True}, status=200)
#         except Exception as e:
#             print(e)
#             return JsonResponse({"response": False}, status=400)

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
            }
            return JsonResponse({"message":"verified", "user":data}, status=200)
        else:
            return JsonResponse({"message":"incorrect otp"}, status=200)
    def post(self, request):
        email = request.data['email']
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
            }
            return JsonResponse(data, status=200)
        except Exception as e:
            user_object = NewUser(email=email)
            user_object.save()
            print(user_object)
            user_email = user_object.email
            data = {
                "id": user_object.id,
                "email": user_email,
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
