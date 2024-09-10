from django.shortcuts import render, redirect
from main.forms import RegisterForm, points_form, email_form
from .models import points_model
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
import urllib
import re
import pandas as pd
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
import yagmail


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def games(request):
    if request.method == 'POST':
        
        
        point_model = points_model()
        points_added = request.POST.get('points')
        
        print(points_added)
        i = 0
        for models in points_model.objects.all():
            print(models.user)
            print(request.user.username)
            if models.user == request.user.username:
                i = 1
                previous_points = models.points
                
                    
                
                models.points = int(previous_points) + int(points_added)
                models.save()
                form = points_form()
               
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
    print(final_scores)
    for models in points_model.objects.all():
        if models.user == request.user.username:
            points = models.points
    form = points_form()
    return render(request, 'games.html', {'form': form, 'top_scores': final_scores, 'points': points})

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
            
            call = requests.get(f"https://www.googleapis.com/civicinfo/v2/representatives?key=AIzaSyDxGsCeJRDMAgqfTVJBpnHpVQ-vE_7K1cI&address={clean_address}")
            response = call.json()
            divisions = response['divisions']
            lis = list(divisions.values())
            reps = {1:'Congressman Davis',2:'Congresswoman Ross',3:'Congressman Murphy',4:'Congresswoman Foushee',5:'Congresswoman Foxx',6:'Congresswoman Manning',7:'Congressman Rouzer',8:'Congressman Bishop', 9:'Congressman Hudson',10:'Congressman McHenry',
                    11:'Congressman Edwards',12:'Congresswoman Adams',13:'Congressman Nickel',14:'Congressman Jackson'}
        
            district = lis[0]['name'] + lis[2]['name'] + lis[7]['name']
            numberss = re.findall(r'\d+', district)
            final = list(map(int, numberss))
            congress_house_member = reps[final[0]]
            house_member = (house.loc[house['District']==final[1], 'Member']).to_string()
            pic_house = house.loc[house['District']==final[1], 'Photo']
            email_house = house.loc[house['District']==final[1], 'Email'].to_string()
            senate_member = senate.loc[senate['District']==final[2], 'Member'].to_string()
            pic_senate = senate.loc[senate['District']==final[2], 'Photo']
            email_senate = senate.loc[senate['District']==final[2], 'Email'].to_string()

            house_member = re.sub(r'[0-9]+', '', house_member)
            email_house = re.sub(r'[0-9]+', '', email_house)
            senate_member = re.sub(r'[0-9]+', '', senate_member)
            email_senate = re.sub(r'[0-9]+', '', email_senate)
            
            context = {house_member:email_house, senate_member: email_senate}

            
            for member, email in context.items():
                email = f"Dear {member}, TESTING TESTING. Thankys! {last_name},{first_name}"      
                 
                yag = yagmail.SMTP('johnstoncolin394@gmail.com', 'fntp cisu fwwd wwbr')
                yag.send('crystallovesyou04@gmail.com','Constituent concerned over PFAS chemicals polluting our water.', email)
            return render(request, 'action.html', context=context)
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




def add_points(request):
    print('connected')
    if request.method == 'POST':
        
        
        point_model = points_model()
        points_added = request.POST.get('points')
        
        print(points_added)
        i = 0
        for models in points_model.objects.all():
            print(models.user)
            print(request.user.username)
            if models.user == request.user.username:
                i = 1
                previous_points = models.points
                
                    
                
                models.points = int(previous_points) + int(points_added)
                models.save()
                return HttpResponseRedirect('')
                    
                
            
        print('sucess')
        return render()
    
    return Response({'status': 'error', 'message': 'User not found'}, status=404)


