from django.shortcuts import render, redirect
from main.forms import RegisterForm
from .models import points_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def games(request):
    return render(request, 'games.html')

def maps(request):
    return render(request, 'maps.html')

def action(request):
    return render(request, 'action.html')

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



@api_view(['POST'])
def add_points(request):
    print('connected')
    points_added = 10
    try:
        point_model = points_model()
        
        for models in points_model.objects.all():
            print(models.user)
            print(request.user.username)
            if models.user == request.user.username:
                print('passed')
                previous_points = models.points
                point_model.points = previous_points + points_added
            point_model.save()
            print('sucess')
        return HttpResponse('sucess', content_type="application/json")
    except User.DoesNotExist:
        return Response({'status': 'error', 'message': 'User not found'}, status=404)

@csrf_exempt
def add_to_model(request):
    print('hi')
    if request.method == 'POST':
        
        data = request.POST.get('data')
        # Process and save data to the model
        point_model = points_model()
        
        for models in points_model.objects.all():
            print(models.user)
            print(request.user.username)
            if models.user == request.user.username:
                print('passed')
                previous_points = models.points
                point_model.points = previous_points + data
            point_model.save()
            print('sucess')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})