from django.db import models
from django.utils import timezone
# import django
from django.conf import settings
from django.utils.timezone import activate

activate(settings.TIME_ZONE)
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        other_fields.setdefault("is_active", True)
        if not email:
            raise ValueError(gettext_lazy("You must provide an email"))
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)
        return self.create_user(email, password, **other_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy("Email Address"), unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    start_Date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email







class Rest(models.Model):
    res_id = models.AutoField(primary_key=True)
    res_name = models.CharField(max_length=122, null=True)
    location = models.CharField(max_length=122, default='Gurugram')
    res_img = models.CharField(max_length=222,null=True)
    rating = models.IntegerField(default=0)
    delivery_time = models.CharField(max_length=122,null=True)
    promo = models.CharField(max_length=122,null=True)
    order_placed = models.BooleanField(default=False)
class RestAdmin(admin.ModelAdmin):
    list_display = ('res_id','res_name','location' ,'res_img' ,'rating' ,'delivery_time' ,'promo','order_placed')

class FoodItem(models.Model):
    res_menu_id = models.ForeignKey(Rest, on_delete=models.CASCADE, null=True)
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=122, null=True)
    price = models.FloatField(blank=True, null=True)
    food_type = models.CharField(max_length=122, null=True)
    cuisine = models.CharField(max_length=122, null=True)
    combo = models.BooleanField(default=False)
    food_img = models.CharField(max_length=222,null=True)

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('food_id','res_menu_id','food_name','price','food_type','cuisine','combo','food_img')

class Order_placed(models.Model):
    userdetail = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True)
    resdet = models.CharField(max_length=122,null=True)
    fooddet = models.CharField(max_length=122,null=True)
class Order_placedAdmin(admin.ModelAdmin):
    list_display = ('userdetail','resdet','fooddet')
class Tags(models.Model):
    food_item_tags = models.ForeignKey(FoodItem, on_delete=models.CASCADE, null=True)
    tag = models.CharField(max_length=122, null=True)

class TagsAdmin(admin.ModelAdmin):
    list_display = ('food_item_tags','tag')


