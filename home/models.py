from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=User)
    FOOD = models.BooleanField(default=False, blank=True)
    TECHNICAL = models.BooleanField(default=False, blank=True)
    TECHNOLOGY = models.BooleanField(default=False, blank=True)
    NEWS = models.BooleanField(default=False, blank=True)
    MOVIES = models.BooleanField(default=False, blank=True)
    HISTORY = models.BooleanField(default=False, blank=True)
    KNOWLEDGE = models.BooleanField(default=False, blank=True)
    FITNESS = models.BooleanField(default=False, blank=True)
    GAMES = models.BooleanField(default=False, blank=True)
    SOCIAL = models.BooleanField(default=False, blank=True)
    ECONOMY = models.BooleanField(default=False, blank=True)
    BUSINESS = models.BooleanField(default=False, blank=True)
    OTHERS = models.BooleanField(default=False, blank=True)

    def __str__(self):
        if self.user == None:
            return "ERROR-CUSTOMER NAME IS NULL"
        return str(self.user)
            # return f'{self.user.username}'



class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name


class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    add = models.CharField(max_length=10000,null=True)
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.user.username



class VerifyEmail(models.Model):
	customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	token=models.UUIDField(default = uuid.uuid4,editable = False)
	is_verified=models.BooleanField(default=False)


