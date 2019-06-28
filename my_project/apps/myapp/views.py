from django.shortcuts import render, HttpResponse,redirect
from .models import users
import bcrypt
from django.contrib.messages import error
import json
import requests
from django.contrib import messages
from . import models
from django.db.models import Q

def index(request):
    return render(request,'myapp/index.html')

def signup(request):
    return render(request,'myapp/signup.html')

def login(request):
    return render(request,'myapp/login.html')
    
def signupp(request):
    #adding the information into the database
    if request.method=="POST":
        errorz=users.objects.basicValid(request.POST)
        if errorz:
            for i in errorz:
                error(request,i)
            return redirect('/signup')
        else:
            new_id=users.objects.register_user(request.POST)
            print(new_id)
            print('*'*50)
            request.session['userid']=new_id
            context={
                'username':users.objects.get(id=new_id).firstname,
                'email':users.objects.get(id=new_id).email
            }
    return render(request,'myapp/reg.html',context)


def loginp(request):
    if request.method=='POST':
        login=users.objects.loginValid(request.POST)
        if login==True:
            new_id=users.objects.get(username=request.POST['username']).id
            request.session['userid']=new_id
            return redirect('/thelogin')
        else:
            for i in login:
                error(request,i)
            return redirect('/login')
    return redirect('/thelogin')

def thelogin(request):
    try:
        if not request.session['userid']:
            return redirect('/login')
    except:
        return redirect('/login')
    else:
        myid=request.session['userid']
        print('*'*50)
        print(myid)
        context={
            'myuserid':users.objects.get(id=myid).id,
            'myuserfirstname':users.objects.get(id=myid).firstname,
            'myuserlastname':users.objects.get(id=myid).lastname,
            'myuseremail':users.objects.get(id=myid).email,   
            "all_beers": models.beers.objects.filter(user=request.session['userid'])
        }
    return render(request,'myapp/dashboard.html',context)

def logout(request):

    try:
        del request.session['userid']
    except:
        redirect('/')
    # del request.session['userid']
    return redirect('/')

def add(request):
    return render(request, 'myapp/add.html')

def addbrew(request):
    print('*'*50)
    try:
        if int(request.POST['rate'])>1:
            errors = users.objects.form_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return render (request, 'myapp/add.html')
            else:
                user = users.objects.get(id=request.session['userid'])
                new_beer = models.beers.objects.create(name=request.POST['beer'], category=request.POST['category'], abv=request.POST['abv'], ibu=request.POST['ibu'], brewery=request.POST['brewery'],rating=request.POST["rate"])
                user.beer.add(new_beer)
            return redirect('/thelogin')
                
    except:
        errors='Please Rate Your Drink'
        error(request,errors)
        return redirect('/add')

def fave_beer(request, beer_id):
    try:
        if not request.session['userid']:
            return redirect('/login')
    except:
        errors={'Please Sign Up or Log In'}
        for i in errors:
            error(request,i)
        return redirect('/login')
    user = users.objects.get(id=request.session['userid'])
    fave = models.beers.objects.get(id=beer_id)
    user.beer.add(fave)    
    return redirect('/thelogin')

def remove(request, user_id):
    user = models.users.objects.get(id = request.session['userid'])
    remove_beer = models.beers.objects.get(id = user_id)
    user.beer.remove(remove_beer)
    return redirect('/thelogin')

def ales(request):
    context = {
        "all_ales": models.beers.objects.filter(Q(category="ipa") | (Q(category="ale")))
    }
    return render(request, 'myapp/ales.html', context)
def lagers(request):
    context = {
        "all_lagers": models.beers.objects.filter(category="lager")
    }
    return render(request, 'myapp/lagers.html', context)
def malts(request):
    context = {
        "all_malts": models.beers.objects.filter(category="malt")
    }
    return render(request, 'myapp/malts.html', context)
def stouts(request):
    context = {
        "all_stouts": models.beers.objects.filter(category="stout")
    }
    return render(request, 'myapp/stouts.html', context)

def show(request, beer_id):
    context = {
        "beer_info": models.beers.objects.get(id=beer_id)
    }
    return render(request, 'myapp/show.html', context)




def searching(request):

    business_id='edcdC4ixlSjPn50WdwSpBQ'
    #Define the API Key, Define the Endpoint, and deefine the Header
    API_KEY='JA-SJIs2e-2ib3JVAqmIMzlWPigODEw0Djc_oKehvjmuvI92e-t-lEmYlZCGW9W3T-En7RQLuTZ9ABm_wLADJ7tw65LamAIjqFiKRA76S7x1kpT6ubtcU1QxVrMSXXYx'
    ENDPOINT='https://api.yelp.com/v3/businesses/search'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}
    # Define the parameters
    PARAMETERS = {'term' : request.POST['searches'],
                'limit':5,
                'radius':10000,
                'location': 'Long Beach'}

    response=requests.get(url= ENDPOINT,params=PARAMETERS,headers=HEADERS)

    business_data=response.json()
    img=[]
    rating=[]
    name=[]
    
    for biz in business_data['businesses']:
        rating.append(biz["rating"])
        name.append(biz['name'])
        img.append(biz['image_url'])
        print(type(img))

    context={
        # 'ratings1':rating[1],
        # 'names1':name[1],
        # 'image1':img[1],
        # 'ratings2':rating[2],
        # 'names2':name[2],
        # 'image2':img[2],
        # 'ratings3':rating[3],
        # 'names3':name[3],
        # 'image3':img[3],
        'namez':name,
        'ratingz':rating,
        'imgz':img

    }
    return render(request,'myapp/searchresult.html',context)

def searching2(request):
    try:
        print('00'*20)
        print(request.POST['beernamez'])

        business_id='edcdC4ixlSjPn50WdwSpBQ'
        #Define the API Key, Define the Endpoint, and deefine the Header
        API_KEY='JA-SJIs2e-2ib3JVAqmIMzlWPigODEw0Djc_oKehvjmuvI92e-t-lEmYlZCGW9W3T-En7RQLuTZ9ABm_wLADJ7tw65LamAIjqFiKRA76S7x1kpT6ubtcU1QxVrMSXXYx'
        ENDPOINT='https://api.yelp.com/v3/businesses/search'
        HEADERS = {'Authorization': 'bearer %s' % API_KEY}
        # Define the parameters
        PARAMETERS = {'term' :request.POST['beernamez'],
                    'limit':1,
                    'radius':40000,
                    'categories' : 'Breweries',
                    'location': 'Anaheim'}

        response=requests.get(url= ENDPOINT,params=PARAMETERS,headers=HEADERS)

        business_data=response.json()
        
        for biz in business_data['businesses']:
            rating=(biz["rating"])
            name=(biz['name'])
            img=(biz['image_url'])
            url=(biz['url'])
            location=(biz['location'])
            price=(biz['price'])
            phone=(biz['phone'])
            print(type(img))

        context={
            'pricez':price,
            'locationz':location,
            'namez':name,
            'ratingz':rating,
            'imgz':img,
            'urlz':url,
            'phonez':phone

        }
        return render(request,'myapp/searchresult.html',context)
    except:
        errors={'error':'Brewery Does Not Exist'}
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/thelogin')
    
