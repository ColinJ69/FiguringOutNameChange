from math import e
from django.shortcuts import render, redirect
from main.forms import RegisterForm, points_form, email_form, loginForm, repForm, resetForm
from .models import points_model, donate_model, newsletter, user_donate_model
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
import urllib
import re
import pandas as pd
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
import yagmail
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from .syn_functions import predict
from urllib.parse import quote_from_bytes
from django.contrib.auth import login
from users.models import User
from django.contrib import messages
import datetime
import random

# Create your views here.
def homepage(request):
    
    if request.method == 'POST':
        
        
        body = request.POST
        if 'userLog' in body:
            print('login')
            
            
            username = body['username']
            password = body['password']
            
          
            user = authenticate(username=username, password=password)
            login(request, user)
                
            return redirect('/')

            
        elif 'userReg' in body:
            print('register')
            form = RegisterForm(request.POST)
            if form.is_valid():
                print('valid')
                user = form.save()
                username = form.cleaned_data['username']
                starting_points = 0
                points = points_model()
                points.user = username
                points.points = starting_points
                points.save()
                login(request, user)

                return redirect('/')
    user = request.user.username
    
    if user == '':
        user = 'None'
        logged_in = False
        points = 0
    else: 
        logged_in = True
    for models in points_model.objects.all():
                if models.user == request.user.username:
                    points = int(models.points)
        
                
                
    current_date = datetime.date.today()  
   
    random.seed(current_date.toordinal())
    new_number = random.randint(1, 17)
    ogged_in = False
    signed_up = False
    if request.user.is_authenticated:
        logged_in = True
        
        
        for i in newsletter.objects.all():
            if i.user == request.user.username:
                signed_up = True
                break
    

    return render(request, 'homepage.html', {'form': loginForm, 'usern': user, 'forms':RegisterForm, 'formr':resetForm, 'points':points, 'logged_in':logged_in,'signed_up':signed_up, 'num':new_number})
from google.oauth2 import id_token
from google.auth.transport import requests
@api_view(('GET',))
def google_sign(request):
    # (Receive token by HTTPS POST)
    # ...
    token = request.body['token']
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), '374367816012-503cj4pjim8oe0obtglknt0b4ajrq1an.apps.googleusercontent.com')

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If the request specified a Google Workspace domain
        # if idinfo['hd'] != DOMAIN_NAME:
        #     raise ValueError('Wrong domain name.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
        # Invalid token
        pass

@api_view(('GET', ))
def get_points(request):
    for models in points_model.objects.all():
            if models.user == request.user.username:
                points = int(models.points)
                
                
                return Response(points)
    return Response(0)
  
            

def games(request):
    logged_in = False
    signed_up = False
    if request.user.is_authenticated:
        logged_in = True
        
        
        for i in newsletter.objects.all():
            if i.user == request.user.username:
                signed_up = True
                break
 
    try:
        i = points_model.objects.all()
        points_dict = {}
        for x in i:
            points_dict[x.user] = x.points
        sorted_dict = {}
        for key in sorted(points_dict, key=points_dict.get, reverse=True):
            sorted_dict[key] = points_dict[key]
 
   
        all_sorted_names = list(sorted_dict.keys())
        top_names = (all_sorted_names)[:9]
        all_sorted_scores = list(sorted_dict.values())
        top_scores = all_sorted_scores[:9]
        ranks = [1,2,3,4,5,6,7,8,9,10]
        final_scores = zip(top_names, top_scores, ranks)
        
        for models in points_model.objects.all():
            if models.user == request.user.username:
                points = models.points
        donated_dollars = 0
        for x in donate_model.objects.all():
            donate = x.dollars
        for models in user_donate_model.objects.all():
            if models.username == request.user.username:
                donated_dollars = models.dollars
        
        form = points_form()
        
        return render(request, 'games.html', {'form': form, 'top_scores': final_scores, 'points': points, 'dollars':donated_dollars, 'donated_dollars':donated_dollars, 'signed_up':logged_in, 'logged_in':logged_in})
    except: 
        form = points_form()
        return render(request, 'games.html', {'form': form, 'top_scores': final_scores, 'points': 'Login to get points', })

def maps(request):
    logged_in = False
    signed_up = False
    if request.user.is_authenticated:
        logged_in = True
        
        
        for i in newsletter.objects.all():
            if i.user == request.user.username:
                signed_up = True
                break
 
    context = {
      'signed_up': signed_up,
      'logged_in': logged_in
        }
    return render(request, 'maps.html', context=context)
from geopy.geocoders import Nominatim 
import requests
def action(request):
    logged_in = False
    signed_up = False
    if request.user.is_authenticated:
        logged_in = True
        
        
        for i in newsletter.objects.all():
            if i.user == request.user.username:
                signed_up = True
                break
 
    
    house = pd.read_excel("C:/Users/johns/OneDrive/Documents/nc_house_members.xlsx")
    senate = pd.read_excel("C:/Users/johns/OneDrive/Documents/nc_senate_members.xlsx")
    if request.method == 'POST':
        req = request.POST
        if 'petForm' in req:
            form = email_form(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                address = form.cleaned_data['address']
                first_name = form.cleaned_data['first']
                last_name = form.cleaned_data['last']
            
                clean_address = urllib.parse.quote(address, safe='/', encoding=None, errors=None)
            
                call = requests.get(f"https://www.googleapis.com/civicinfo/v2/representatives?key=AIzaSyDxGsCeJRDMAgqfTVJBpnHpVQ-vE_7K1cI&address={clean_address}")
                response = call.json()
                divisions = response['divisions']
                lis = list(divisions.values())
                reps = {1:['Donald Davis','https://dondavis.house.gov/contact'],2:['Deborah Ross','https://rossforms.house.gov/forms/writeyourrep/'],3:['Greg Murphy','https://gregmurphyforms.house.gov/contact/email-me.htm'],4:['Valerie Foushee','https://foushee.house.gov/contact'],5:['Virginia Foxx', 'https://foxx.house.gov/connect/default.aspx'],6:['Kathy Manning','https://manning.house.gov/contact'],7:['David Rouzer','https://rouzer.house.gov/contact/'],8:['Dan Bishop', 'https://danbishop.house.gov/address_authentication?form=/contact'], 9:['Richard Hudson', 'https://hudson.house.gov/address_authentication?form=/contact'],10:['Patrick McHenry', 'https://mchenry.house.gov/contact/zipauth.htm'],
                        11:['Chuck Edwards', 'https://edwards.house.gov/contact'],12:['Alma Adams', 'https://adamsforms.house.gov/contact/'],13:['Wiley Nickel', 'https://nickel.house.gov/contact/'],14:['Jeff Jackson', 'https://jeffjackson.house.gov/contact']}
           
                district = lis[0]['name'] + lis[2]['name'] + lis[6]['name']
                numberss = re.findall(r'\d+', district)
                final = list(map(int, numberss))
                congress_house_member = reps[final[0]]
                house_member = (house.loc[house['District']==final[1], 'Member']).to_string()
            
                email_house = house.loc[house['District']==final[1], 'Email'].to_string()
                senate_member = senate.loc[senate['District']==final[2], 'Member'].to_string()
                c_member = congress_house_member[0]
                c_link = congress_house_member[1]
                email_senate = senate.loc[senate['District']==final[2], 'Email'].to_string()
                congress_member = re.sub(r'[0-9]+', '', c_member)
                house_member = re.sub(r'[0-9]+', '', house_member)
                email_house = re.sub(r'[0-9]+', '', email_house)
                senate_member = re.sub(r'[0-9]+', '', senate_member)
                email_senate = re.sub(r'[0-9]+', '', email_senate)
            
                
                return render(request, 'action.html', {'submitted': True, 'house': house_member, 'senate': senate_member, 'congress': congress_member, 'link': c_link, 'email': i})
        elif 'repForm' in req:
            form = repForm(request.POST)
            if form.is_valid():
                address = form.cleaned_data['address']
                print(address)
                pattern = r'[a-zA-Z]'
                clean_address = urllib.parse.quote(address, safe='/', encoding=None, errors=None)                  
                if not re.search(pattern, address):
                    lat = float(address.split(',')[0])
                    lng = float(address.split(',')[1])
                    print(lat, lng)
                    geolocator = Nominatim(user_agent="HydroHaven") 
                    location = geolocator.reverse((lat, lng), exactly_one=True) 
                    clean_address = location.address
                
                call = requests.get(f"https://www.googleapis.com/civicinfo/v2/representatives?key=AIzaSyDxGsCeJRDMAgqfTVJBpnHpVQ-vE_7K1cI&address={clean_address}")
                response = call.json()
               
                divisions = response['divisions']
                lis = list(divisions.values())
                
                reps = {1:['Donald Davis','https://dondavis.house.gov/contact', "RepImages/DonaldDavis.jpeg"],
                        2:['Deborah Ross','https://rossforms.house.gov/forms/writeyourrep/',"RepImages/DeborahRoss.jpeg" ],
                        3:['Greg Murphy','https://gregmurphyforms.house.gov/contact/email-me.htm',"RepImages.GregoryMurphy.jpeg"],
                        4:['Valerie Foushee','https://foushee.house.gov/contact', "RepImages/ValerieFoushee.jpeg"],
                        5:['Virginia Foxx', 'https://foxx.house.gov/connect/default.aspx', "RepImages/VirginiaFoxx.jpeg"],
                        6:['Kathy Manning','https://manning.house.gov/contact',"RepImages/KathyManning.jpeg"]
                        ,7:['David Rouzer','https://rouzer.house.gov/contact/',"RepImages/DavidRouzer.jpeg"],
                        8:['Dan Bishop', 'https://danbishop.house.gov/address_authentication?form=/contact',"RepImages/DanBishop.jpeg"], 
                        9:['Richard Hudson', 'https://hudson.house.gov/address_authentication?form=/contact',"RepImages/RichardHudson.jpeg"],
                        10:['Patrick McHenry', 'https://mchenry.house.gov/contact/zipauth.htm', "RepImages/PatrickMcHenry.jpeg"],
                        11:['Charles Edwards', 'https://edwards.house.gov/contact', "RepImages/CharlesEdwards.jpeg"],
                        12:['Alma Adams', 'https://adamsforms.house.gov/contact/',"RepImages/AlmaAdams.jpeg"],
                        13:['Wiley Nickel', 'https://nickel.house.gov/contact/', "RepImages/WileyNickel.jpeg"],
                        14:['Jeff Jackson', 'https://jeffjackson.house.gov/contact',"RepImages/JeffreyJackson.jpeg"]
                        }
                
           
                district = lis[0]['name'] + lis[2]['name'] + lis[6]['name']
                numberss = re.findall(r'\d+', district)
                final = list(map(int, numberss))
                congress_house_member = reps[final[0]]
                house_member = (house.loc[house['District']==final[1], 'Member']).to_string()
            
                email_house = house.loc[house['District']==final[1], 'Email'].to_string()
                senate_member = senate.loc[senate['District']==final[2], 'Member'].to_string()
                c_member = congress_house_member[0]
                c_link = congress_house_member[1]
                email_senate = senate.loc[senate['District']==final[2], 'Email'].to_string()
                congress_member = re.sub(r'[0-9]+', '', c_member)
                house_member = re.sub(r'[0-9]+', '', house_member)
                email_house = re.sub(r'[0-9]+', '', email_house)
                senate_member = re.sub(r'[0-9]+', '', senate_member)
                email_senate = re.sub(r'[0-9]+', '', email_senate)
                image_senate = senate.loc[senate['District']==final[2], 'Image'].item()
                image_house = house.loc[house['District']==final[1], 'Image'].item()
                image_congress = congress_house_member[2]
                print(image_senate, image_house, image_congress)
                context = {'rep_sub': True,
                           'house': house_member,
                          'senate': senate_member,
                         'congress': congress_member,
                        'link': c_link,
                        'sen_email': email_senate, 
                        'house_email': email_house,
                        'housepic': image_house,
                        'senpic': image_senate,
                        'conpic': image_congress,
                        'signed_up': signed_up,
                            'logged_in': logged_in
                        }
                return render(request, 'action.html', context = context)
    rep_form = repForm()
    form = email_form()
    context = {'rep_sub': False,
                        'signed_up': signed_up,
                        'logged_in': logged_in,
                        'form':form,
                        'repform':rep_form,
                        }
   
    return render(request, 'action.html', context=context)

def register(request):
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            starting_points = 0
            points = points_model()
            points.user = username
            points.points = starting_points
            user_donate = user_donate_model()
            user_donate.username = username
            user_donate.dollars = 0
            user_donate.save()
            points.save()
            login(request, user)

            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'create_account.html', {'form': form})



@csrf_exempt
def add_points(request):
    
    if request.method == 'POST':
        
        
       
        
        data = json.loads(request.body)
      
        for models in points_model.objects.all():
            
            if models.user == request.user.username:
                i = 1
                previous_points = models.points
                
                    
                
                models.points = int(previous_points) + int(data['points'])
                models.save()
                return HttpResponseRedirect('')
                    
                
       
        return Response('yippee')
    
    return Response({'status': 'error', 'message': 'User not found'}, status=404)

@api_view(('POST', 'GET'))
@csrf_exempt
def synthesize(request):
    try:
        
        #for models in points_model.objects.all():
         #       if models.user == request.user.username:
         #           points = int(models.points)
         #           models.points = (points - 500)
         #           models.save()
        body_datas = request.data
    
    
        add = body_datas['add']
        depth = body_datas['depth']
        pattern = r'[a-zA-Z]'
        clean_address = urllib.parse.quote(add, safe='/', encoding=None, errors=None)
        if not re.search(pattern, add):
            lat = float(add.split(',')[0])
            lng = float(add.split(',')[1])
            print(lat, lng)
            geolocator = Nominatim(user_agent="hydrohaven") 
            location = geolocator.reverse((lat, lng), exactly_one=True) 
            add = location.address
        print(add)
        result = predict(add, depth)
        
        return HttpResponse(result)
    except:
        return HttpResponse('2')

def guides(request):
    logged_in = False
    signed_up = False
    if request.user.is_authenticated:
        logged_in = True
        
        
        for i in newsletter.objects.all():
            if i.user == request.user.username:
                signed_up = True
                break
    context = {
      'signed_up': signed_up,
      'logged_in': logged_in
        }
    return render(request, 'guides.html', context=context)


@api_view(('POST', 'GET'))
@csrf_exempt
def donate(request):
  
    if request.method == 'POST':
 
        if request.user.username == '':
            return JsonResponse({'status':'nameError'})
        for models in points_model.objects.all():
            
            if models.user == request.user.username:
                
                previous_points = models.points
                if models.points < 1000:
                    return JsonResponse({'status': 'Bad'})
                models.points = int(previous_points) - 1000
                models.save()
                print(models.points)
                for u in user_donate_model.objects.all():
                    if u.username == request.user.username:
                    
                        u.dollars = int(u.dollars) + 1
                        u.save()
                    else:
                        model = user_donate_model()
                        model.username = request.user.username
                        model.dollars = 1
                for m in donate_model.objects.all():
                    m.dollars = int(m.dollars) + 1
                    m.save()
                    return JsonResponse({'status': 'Good'})
                    
                
            
     
        return Response('yippee')
    
    return Response({'status': 'error', 'message': 'User not found'}, status=404)





def logins(request):
    
    form = loginForm()
    forms = RegisterForm()

    if request.method == "POST":
        body = request.POST
        if 'userLog' in body:
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            # Check if a user with the provided username exists
            if not User.objects.filter(username=username).exists():
                # Display an error message if the username does not exist
                messages.error(request, 'Invalid Username')
                return redirect('/logins')
        
            # Authenticate the user with the provided username and password
            user = authenticate(username=username, password=password)
        
            if user is None:
                # Display an error message if authentication fails (invalid password)
                messages.error(request, "Invalid Password")
                return redirect('/logins')
            else:
                # Log in the user and redirect to the home page upon successful login
                login(request, user)
                return redirect('/')
        
    # Render the login page template (GET request)
    return render(request, 'login.html', {'form':form})

def art_helene(request):
    return render(request, 'art_helene.html')

def logouts(request):
    logout(request)
    return redirect('/')

def news(request):
    logged_in = False
    signed_up = False
    if request.user.is_authenticated:
        logged_in = True
        
        
        for i in newsletter.objects.all():
            if i.user == request.user.username:
                signed_up = True
                break
 
    context = {
      'signed_up': signed_up,
      'logged_in': logged_in
        }
    
    return render(request, 'news.html', context=context)


@api_view(('POST', 'GET'))
@csrf_exempt
def newsletter_signup(request):
    print('hi')
    data = request.data
    if 'email' in data:
        print('hi')
        email = data['email']
        model = newsletter()
        model.user = 'NoName'
        model.email = email
        model.save()
        print('done')
        return HttpResponseRedirect('')
    response = data['register']
    if response == True:
        users = User.objects.all()
        username = request.user.username
        
        email = ''
        for user in users:
            
            if str(user) == str(username):
                print('yay')
                email = user.email
                model = newsletter()
                model.user = request.user.username
                model.email = email 
                model.save()
                return HttpResponseRedirect('')
             
        model = newsletter()
        model.user = request.user.username
        model.email = email 
        model.save()
        return HttpResponseRedirect('')
    if response == False:
        model = newsletter()
        for models in newsletter.objects.all():
            if models.user == request.user.username:
                models.delete()
                print('deleted')
        
        return HttpResponseRedirect('')
    
import base64
@api_view(('POST','GET'))
@csrf_exempt
def get_questions(request):
    data = request.data 
    
    q = data['q']
    q = int(base64.b64decode(q))
    
    
    with open("C:/Users/johns/OneDrive/Documents/Desktop/PFAS_Web/Web/main/questions.json") as file:
        data = json.load(file)
        
        response = data[q]
        s = json.dumps(response)
        hi = base64.b64encode(s.encode('utf-8'))
       
    return Response(hi)
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
@api_view(('POST','GET'))
def post_story(request):
    data = request.data
    data = str(data['story'])
    html = render_to_string(f'emails/art-{data}.html')
    for i in newsletter.objects.all():
        
        msg = EmailMultiAlternatives(
        "Saturday story",
        'penis',
        "hydrohavennc@gmail.com",
        [i.email],
        
        )   
        msg.attach_alternative(html, "text/html")
        msg.send()
        
    return Response({'Sigma':'Gyatt'})

def unsubcribe(request):
    return render(request, 'unsubscribe.html')

@api_view(('POST','GET'))
def newsletter_unsub(request):
    data = request.data
    data = str(data['email'])

    print(data)
    
    for i in newsletter.objects.all():
        print(i.email)
        if i.email == data:
            i.delete()
            return Response('1')
    
    return Response('0')


