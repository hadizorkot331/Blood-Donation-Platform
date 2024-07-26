import sys
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

sys.path.append("..")
from constants import BLOOD_TYPES, HOSPITALS_AS_CHOICES


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, default=("A+"))
    hospital = models.CharField(
        max_length=150,
        choices=HOSPITALS_AS_CHOICES,
        default="American University of Beirut Medical Center",
    )
    description = models.TextField(blank=False, default="")
    phone_number = PhoneNumberField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True, blank=False)
    fullfilled = models.BooleanField(default=False)
