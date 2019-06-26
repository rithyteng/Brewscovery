from django.db import models
import re
from django.shortcuts import redirect
import bcrypt

EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class usersManager(models.Manager):

    def display_detailed_values(self):
        return [u.__dict__ for u in self.all()]
    
    def register_user(self,form):
        hashed=bcrypt.hashpw(form['password'].encode(),bcrypt.gensalt())
        the_user=self.create(firstname=form['firstname'],lastname=form['lastname'],email=form['email'],username=form['username'],password=hashed)
        return the_user.id


    def basicValid(self,form):
        errors=[]

        if len(form['username'])<6:
            errors.append('Username Requires At Least 6 Characters ')
        if len(form['firstname'])<2:
            errors.append("Invalid First Name")
        if len(form['lastname'])<2:
            errors.append('Invalid Last Name')
        if not form['password'] == form['cpassword']:
            errors.append('Password Does Not Match')

        if not EMAIL_REGEX.match(form['email']):
            errors.append('Invalid Email')
        
        result=self.filter(email=form['email'])
        result2=self.filter(username=form['username'])

        if result:
            errors.append('Email is already in use')
        if result2:
            errors.append('Username is already in use')
        return errors
    
    def loginValid(self,form):
        errors=[]
        checkemail=self.filter(username=form['username'])
        if not checkemail:
            errors.append('Invalid Username or Password')
        else:
            for i in checkemail:
                hashed=i.password
            #Check Password
            if bcrypt.checkpw(form['password'].encode(),hashed.encode()):
                return True
            else:
                errors.append('Invalid Username or Password')
        return errors



class users(models.Model):
    username=models.CharField(max_length=55)
    firstname=models.CharField(max_length=55)
    lastname=models.CharField(max_length=55)
    email=models.CharField(max_length=55)
    password=models.CharField(max_length=55)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=usersManager()





# Create your models here.
