import sys
from django.db import models
from django.contrib.auth.models import User


sys.path.append("..")
from constants import BLOOD_TYPES, CAZAS_AS_CHOICES


# Create your models here.
class Profile(models.Model):
    """
    Django offers a default user model which should be used in most cases due to the ability to save, login, logout and access the user easily through the ORM
    When extra fields are required for the user model, Django recommends to create a new model with a one to one relationship to the user model
    This model stores information needed about each user which is not available in the default user model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, default=("A"))
    caza = models.CharField(
        max_length=25, choices=CAZAS_AS_CHOICES, default=("Beirut"), blank=False
    )
    notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}, {self.blood_type}, {self.caza}"
