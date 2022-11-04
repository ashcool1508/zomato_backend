from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Rest, RestAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(NewUser)
admin.site.register(Order_placed,Order_placedAdmin)
