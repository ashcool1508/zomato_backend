from django.urls import path, include
from .views import *

urlpatterns = [

    path('login/', LoginView.as_view()),
    path('all_res/', AllRes.as_view()),
    path('all_res_dishes/', ResfoodItemsList.as_view()),
    # path('order_placed/',),
    # path('set_food_tag/', ),
]