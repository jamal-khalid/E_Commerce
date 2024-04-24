import json
import random
import requests
from .models import OTP 
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_to_phone(phone_number):
    otp = generate_otp()
    OTP.objects.create(phone_number=phone_number, otp_code=otp)
    # URL to the Django server endpoint responsible for handling OTP sending
    # url = 'http://127.0.0.1:8000/send_otp/'
    # url = f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone_number}/{otp}/jamal'

    url = f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone_number}/AUTOGEN'.format(api_key=settings.API_KEY)

    # Data payload to be sent in the POST request

    # this is used with 2factor verification 
    # data = {
    #     'apikey':settings.API_KEY,
    #     'to': phone_number,
    #     'message': f"Your Otp For Login Is {otp}"
    # }

    # url = 'https://2factor.in/API/R1/'
    payload = {
        'module': 'TRANS_SMS',
        'apikey': settings.API_KEY,
        'to': ','.join(phone_number),
        'from': settings.SENDER_ID,
        'msg': f'Your Verification Code is {otp}'
    }

    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(otp)
            return otp  # Return the OTP if sending was successful
    except requests.exceptions.RequestException as e:
        print(f"Error sending OTP: {e}")

    return None  # Return None if sending failed

def verify_otp(phone_number, otp_entered):
    try:
        otp = OTP.objects.get(phone_number=phone_number, otp_code=otp_entered, is_verified=False)
        otp.is_verified = True
        otp.save()
        return True
    except OTP.DoesNotExist:
        return False
