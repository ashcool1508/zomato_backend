from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Rest, RestAdmin)
admin.site.register(Tags, TagAdmin)
admin.site.register(NewUser)