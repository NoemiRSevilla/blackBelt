from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        bcrypt.hashpw('test'.encode(), bcrypt.gensalt())
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "<div class='ohno'>First name should at least be 2 characters</div>"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors["first_name"] = "<div class='ohno'>First name must contain only letters</div>"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "<div class='ohno'>Last name should at least be 2 characters</div>"
        else:
            if not NAME_REGEX.match(postData['last_name']):
                errors["last_name"] = "<div class='ohno'>Last name must contain only letters</div>"
        if len(postData['email']) < 1:
            errors["email"] = "<div class='ohno'>Email required</div>"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "<div class='ohno'>Must enter valid email</div>"
        if len(postData['birthdate']) < 1:
            errors["birthdate"] = "<div class='ohno'>Birthdate required</div>"
        else:
            birthdate = datetime.strptime(postData['birthdate'], "%Y-%m-%d")
            present = datetime.now()
            if ((present - birthdate).days/365 < 13):
                errors['birthdate'] = "<div class='ohno'>You have to at least be 13 years old to register</div>"
        try:
            User.objects.get(email=postData['email'])
            errors['email'] = "<div class='ohno'>Email already registered</div>"
        except:
            pass
        if len(postData['password']) < 1:
            errors['password'] = "<div class='ohno'>Password required</div>"
        else:
            if len(postData['password']) < 8:
                errors['password'] = "<div class='ohno'>Password has to be at least 8 characters</div>"
        if postData['confirmpassword'] != postData['password']:
            errors['confirmpassword'] = "<div class='ohno'>Password has to match</div>"
        return errors
    def login_validator(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData['email'])
        except:
            errors['password'] = "<div class='ohno'>You could not be logged in</div>"
            return errors
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            return errors
        else:
            errors['password'] = "<div class='ohno'>You could not be logged in</div>"
            return errors

    def edit_user_validator(self, postData, request):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "<div class='ohno'>First name required</div>"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors["first_name"] = "<div class='ohno'>First name must contain only letters</div>"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "<div class='ohno'>Last name required</div>"
        else:
            if not NAME_REGEX.match(postData['last_name']):
                errors["last_name"] = "<div class='ohno'>Last name must contain only letters</div>"
        if len(postData['email']) < 1:
            errors["email"] = "<div class='ohno'>Email required</div>"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "<div class='ohno'>Must enter valid email</div>"
        if request.session['username'] == postData['email']:
            pass
        else:
            try:
                User.objects.get(email=postData['email'])
                errors['email'] = "<div class='ohno'>Email already registered</div>"
            except:
                pass
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birthdate = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __repr__(self):
        return f"ID: {self.id}, First Name: {self.first_name}, Last Name: {self.last_name}, Email: {self.email}"

class QuoteManager(models.Manager):
    def quote_validate(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors["author"] = "<div class='ohno'>Required. More than 3 characters necessary</div>"
        if len(postData['quote']) < 10:
            errors["quote"] = "<div class='ohno'>Required. More than 10 characters necessary</div>"
        return errors

class Quote(models.Model):
    uploaded_by = models.ForeignKey(User, related_name ="quotes_uploaded")
    author = models.CharField(max_length=100)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    users_who_like = models.ManyToManyField(User, related_name="liked_quotes")
    objects = QuoteManager()