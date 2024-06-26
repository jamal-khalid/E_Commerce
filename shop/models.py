from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Product(models.Model):
    product_id = models.AutoField,
    product_name=models.CharField(max_length=20, default="" )
    description=models.CharField(max_length=300 ,default="")
    publish_date = models.DateField(default="")
    price=models.IntegerField(default="0" )
    categary=models.CharField(max_length=50 , default="")
    subcategary=models.CharField(max_length=50 , default="")
    image=models.ImageField( upload_to="shop/images" ,default="")

    def __str__(self):
        return self.product_name
    

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=50)
    desc=models.CharField(max_length=500)


    def __str__(self):
        return self.name
    
class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=200)
    adress=models.CharField(max_length=500)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pin_code=models.CharField(max_length=100)

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    time_stamp=models.DateField(auto_now_add=True)
    # time=models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[:7]+"...." 
    

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
    
