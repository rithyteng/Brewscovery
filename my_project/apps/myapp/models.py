from django.db import models
import re
from django.shortcuts import redirect
import bcrypt

EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class usersManager(models.Manager):

    def display_detailed_values(self):
        return [u.__dict__ for u in self.all()]
    #register user
    def register_user(self,form):
        hashed=bcrypt.hashpw(form['password'].encode(),bcrypt.gensalt())
        the_user=self.create(firstname=form['firstname'],lastname=form['lastname'],email=form['email'],username=form['username'],password=hashed)
        return the_user.id


    def basicValid(self,form):
        errors=[]
        #validates registration form
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

    #validate login, checks if username is in db along w pw
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

    def form_validator(self, postData):
        errors = {}
        if len(postData['beer']) < 3:
            errors['beer'] = "Beer must be at least 3 characters"
        if len(postData['category']) < 3:
            errors['category'] = "Category should be at least 3 characters"
        if len(postData['brewery']) < 3:
            errors['brewery'] = "Brewery should be at least 3 characters"
        if len(postData['abv']) < 1:
            errors['abv'] = "Please input ABV"
        if len(postData['ibu']) < 1:
            errors['ibu'] = "Please input IBU value"
            # if not postData['rate']:
            # errors['rate'] = "Please input rating"
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


class beers(models.Model):
    name = models.CharField(max_length = 45)
    category = models.CharField(max_length = 45)
    abv = models.DecimalField(max_digits=3, decimal_places=1)
    ibu = models.DecimalField(max_digits=4, decimal_places=1)
    brewery = models.CharField(max_length = 45)
    user = models.ManyToManyField(users, related_name="beer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)


class breweries(models.Model):
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






