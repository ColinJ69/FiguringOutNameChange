from django.shortcuts import render, redirect
from main.forms import RegisterForm, points_form, email_form, loginForm
from .models import points_model, donate_model
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
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
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def homepage(request):
    
    return render(request, 'homepage.html')
@api_view(('GET', ))
def get_points(request):
    for models in points_model.objects.all():
            if models.user == request.user.username:
                points = int(models.points)
                
                
                return Response(points)
    return Response(0)
  
            

def games(request):
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
        form = points_form()
        return render(request, 'games.html', {'form': form, 'top_scores': final_scores, 'points': points})
    except: 
        form = points_form()
        return render(request, 'games.html', {'form': form, 'top_scores': final_scores, 'points': 'Login to get points'})

def maps(request):
    return render(request, 'maps.html')

def action(request):
    house = pd.read_excel("C:/Users/johns/OneDrive/Documents/nc_house_members.xlsx")
    senate = pd.read_excel("C:/Users/johns/OneDrive/Documents/nc_senate_members.xlsx")
    if request.method == 'POST':
        form = email_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            first_name = form.cleaned_data['first']
            last_name = form.cleaned_data['last']
            
            clean_address = urllib.parse.quote(address, safe='/', encoding=None, errors=None)
            
            call = requests.get(f"https://www.googleapis.com/civicinfo/v2/representatives?key=xxxxxxxxxxxxxxxxxx&address={clean_address}")
            response = call.json()
            divisions = response['divisions']
            lis = list(divisions.values())
            reps = {1:'Congressman Davis',2:['Congresswoman Ross','https://rossforms.house.gov/forms/writeyourrep/'],3:['Congressman Murphy','https://gregmurphyforms.house.gov/contact/email-me.htm'],4:['Congresswoman Foushee','https://foushee.house.gov/contact'],5:['Congresswoman Foxx', 'https://foxx.house.gov/connect/default.aspx'],6:['Congresswoman Manning','https://manning.house.gov/contact'],7:['Congressman Rouzer','https://rouzer.house.gov/contact/'],8:['Congressman Bishop', 'https://danbishop.house.gov/address_authentication?form=/contact'], 9:['Congressman Hudson', 'https://hudson.house.gov/address_authentication?form=/contact'],10:['Congressman McHenry', 'https://mchenry.house.gov/contact/zipauth.htm'],
                    11:['Congressman Edwards', 'https://edwards.house.gov/contact'],12:['Congresswoman Adams', 'https://adamsforms.house.gov/contact/'],13:['Congressman Nickel', 'https://nickel.house.gov/contact/'],14:['Congressman Jackson', 'https://jeffjackson.house.gov/contact']}
           
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
            
            context = {house_member:email_house, senate_member: email_senate}
            i = f'Dear {congress_member}, I hope this letter finds you well. I am writing to express my concern regarding the presence of per- and polyfluoroalkyl substances (PFAS) in our local water systems. As a resident of your constituency, I am increasingly alarmed by the growing body of evidence highlighting the adverse health effects associated with PFAS exposure. PFAS, often referred to as forever chemicals, are persistent in the environment and have been linked to serious health issues, including cancer, liver damage, and immune system disruption. Recent studies have shown that PFAS contamination is widespread in North Carolina, affecting numerous communities and water sources. This is particularly troubling given the essential role that clean water plays in our daily lives and overall well-being. I urge you to take immediate and decisive action to address this pressing issue. So please, support legistlation backing PFAS clean ups, hold polluters accountable, and help raise public concern. Thank you, {first_name}, {last_name}'
                
            for member, emails in context.items():
                email_text =f'Dear {member}, I hope this letter finds you well. I am writing to express my concern regarding the presence of per- and polyfluoroalkyl substances (PFAS) in our local water systems. As a resident of your constituency, I am increasingly alarmed by the growing body of evidence highlighting the adverse health effects associated with PFAS exposure. PFAS, often referred to as forever chemicals, are persistent in the environment and have been linked to serious health issues, including cancer, liver damage, and immune system disruption. Recent studies have shown that PFAS contamination is widespread in North Carolina, affecting numerous communities and water sources. This is particularly troubling given the essential role that clean water plays in our daily lives and overall well-being. I urge you to take immediate and decisive action to address this pressing issue. So please, support legistlation backing PFAS clean ups, hold polluters accountable, and help raise public concern. Thank you, {first_name}, {last_name}'
                

            
            
                   
                 
                yag = yagmail.SMTP(email, 'xxxxxxxxxxxxxx')
                yag.send(emails, 'Constituent concerned over pfas pollution', email_text)
            return render(request, 'action.html', {'submitted': True, 'house': house_member, 'senate': senate_member, 'congress': congress_member, 'link': c_link, 'email': i})
    form = email_form()
    return render(request, 'action.html', {'form': form})

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
            points.save()
            login(request, user)

            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



@csrf_exempt
def add_points(request):
    
    if request.method == 'POST':
        
        
        point_model = points_model()
        
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
    
    for models in points_model.objects.all():
            if models.user == request.user.username:
                points = int(models.points)
                models.points = (points - 500)
                models.save()
    body_datas = request.data
     
    add = body_datas['add']
    depth = body_datas['depth']
    

    result = predict(add, depth)
    
    return HttpResponse(result)

def guides(request):
    return render(request, 'guides.html')


@api_view(('POST', 'GET'))
@csrf_exempt
def donate(request):
  
    if request.method == 'POST':
 
        point_model = points_model()
      
        for models in points_model.objects.all():
            
            if models.user == request.user.username:
                
                previous_points = models.points
          
                models.points = int(previous_points) - 1000
                models.save()
                for m in donate_model.objects.all():
                    m.dollars = int(m.dollars) + 1
                    m.save()
                    return HttpResponseRedirect('')
                    
                
            
     
        return Response('yippee')
    
    return Response({'status': 'error', 'message': 'User not found'}, status=404)





def logins(request):
    form = loginForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
      
        if not User.objects.filter(username=username).exists():
   
            messages.error(request, 'Invalid Username')
            return redirect('/logins')
        
       
        user = authenticate(username=username, password=password)
        
        if user is None:
          
            messages.error(request, "Invalid Password")
            return redirect('/logins')
        else:

            login(request, user)
            return redirect('/')

    return render(request, 'login.html', {'form':form})
