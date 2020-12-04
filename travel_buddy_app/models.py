from django.db import models
import re, bcrypt
from datetime import datetime

class LoginManager(models.Manager):

    def registerValidator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name must be at least 3 characters"
        if len(postData['username']) < 3:
            errors['username'] = "Username must be at least 3 characters"
        if len(postData['password']) < 8:
            errors['passwordlength'] = "Password must be at least 8 characters"
        if postData['password'] != postData['cpassword']:
            errors['password'] = "These passwords do not match"
        return errors

    def loginValidator(self, postData):
        errors = {}
        usernameExists = User.objects.filter(username = postData['username'])
        if len(usernameExists) == 0:
            errors['usernameNotFound'] = "This username was not found. Please register first."
        else:
            user = usernameExists[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Password does not match"
        if len(postData['password']) < 8:
            errors['passwordlength'] = "Password must be at least 8 characters"
        return errors

class tripManager(models.Manager):

    def tripValidator(self, postData):
        errors = {}
        if len(postData['destination']) == 0:
            errors['destlength'] = "Destination cannot be empty"
        if len(postData['country']) == 0:
            errors['country'] = "Country cannot be empty"
        if len(postData['description']) == 0:
            errors['desclength'] = "Description cannot be empty"
        if len(postData['travelstart']) == 0:
            errors['startlength'] = "Starting date required"
        if len(postData['travelend']) == 0:
            errors['endlength'] = "End date required"
        if postData['travelstart'] > postData['travelend']:
            errors['travelback'] = "Starting time must be before end"
        today = datetime.today().strftime('%Y-%m-%d')
        if postData['travelstart'] < today:
            errors['invalidstartdate'] = "Start date cannot be before today"
        
        return errors


class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    country = models.CharField(max_length = 255, null=True)
    description = models.CharField(max_length = 255)
    joiner = models.ManyToManyField(User, related_name='join_trip')
    uploader = models.ForeignKey(User, related_name='trips', on_delete = models.CASCADE)
    travelstart = models.DateField()
    travelend = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = tripManager()