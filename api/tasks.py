import random
from celery import shared_task
from .models import Device
from decimal import Decimal

@shared_task
def increment_hourmeter():
    devices = Device.objects.all()
    for device in devices:
        # Increment hourmeter by 1
        device.hourmeter += 1  # This adds 1 to the current hourmeter value
        
        # Simulate GPS data
        device.latitude = round(random.uniform(-90.0, 90.0), 6)
        device.longitude = round(random.uniform(-180.0, 180.0), 6)
        device.speed = round(random.uniform(0, 120), 2)
        device.temperature = round(random.uniform(-30, 50), 2)

        # Save the updated device data
        device.save()
