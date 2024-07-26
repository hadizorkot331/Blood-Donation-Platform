import sys
from django.db import models
from django.contrib.auth.models import User


sys.path.append("..")
from constants import BLOOD_TYPES, CAZAS_AS_CHOICES


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, default=("A"))
    caza = models.CharField(
        max_length=25, choices=CAZAS_AS_CHOICES, default=("Beirut"), blank=False
    )

    def __str__(self):
        return f"{self.user.username}, {self.blood_type}, {self.caza}"
