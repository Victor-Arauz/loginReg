from django.contrib.messages.api import error
from django.db import models
import re
import bcrypt
from django.shortcuts import redirect
        

class UserManager(models.Manager):

    def loginValidator(self, formData):

        errors = {}
        matchingEmail = User.objects.filter(email = formData['email'])

        if len(formData['email']) < 1:
            errors['emailRequired'] = 'Email field must be filled out!'

        elif len(matchingEmail) == 0:
            errors['emailNotfound'] = 'Email is not registered. Please register first!'
        
        if len(formData['password']) < 8:
            errors['passwordRequired'] = 'Password must be at least 8 characters long!'

        if not bcrypt.checkpw(formData['password'].encode(), matchingEmail[0].password.encode()):
            errors['passwordWrong'] = 'Password is incorrect!'

            
        return errors


    def registrationValidator(self, formData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        matchingEmail = User.objects.filter(email = formData['email'])

        if len(formData['first_name']) < 2:
            errors['first_nameRequired'] = "First Name should be at least 2 characters long!"

        if len(formData['last_name']) < 2:
            errors['last_nameRequired'] = 'Last Name should be at least 2 characters long!'

        if len(formData['email']) < 1:
            errors['emailRequired'] = 'Email field must be filled out!'

        elif not EMAIL_REGEX.match(formData['email']):    # test whether a field matches the pattern            
            errors['emailInvalid'] = "Invalid email address!"

        elif len(matchingEmail) > 0:
            errors['emailTaken'] = "This email is already taken!"
            
        
        if len(formData['password']) < 8:
            errors['passwordRequired'] = 'Password must be at least 8 characters long!'

        if formData['password'] != formData['confirm_password']:
            errors['passwordMatch'] = 'Passwords must match!'


        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length= 60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"