from twilio.rest import Client 
import random
from django.conf import settings 

def send_otp(mobile):
    otp = random.randint(1000, 9999)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=f'+91{mobile}'
    )
    
    return otp