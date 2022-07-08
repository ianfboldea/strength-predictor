import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import generic

from .models import WorkoutWeek

class IndexView(generic.ListView):
    template_name = 'authentication/index.html'
    context_object_name = 'workouts_list'

    def post(self, request):
        end_date = request.POST.get('end_date')
        total_calories = request.POST.get('total_calories')
        total_sleep = request.POST.get('total_sleep')
        total_chest = request.POST.get('total_chest')
        total_shoulders = request.POST.get('total_shoulders')
        total_triceps = request.POST.get('total_triceps')
        total_protein = request.POST.get('total_protein')
        total_carbs = request.POST.get('total_carbs')
        bench_max = request.POST.get('bench_max')

        new_workout = WorkoutWeek.objects.create(
            end_date=end_date, 
            total_calories=total_calories, 
            total_sleep=total_sleep,
            total_chest=total_chest,
            total_shoulders=total_shoulders,
            total_triceps=total_triceps,
            total_protein=total_protein,
            total_carbs=total_carbs,
            bench_max=bench_max
        )

        new_workout.save()

        messages.success(request, 'Workout Added.')

        return redirect('authentication:index')

    def get_queryset(self):
        return WorkoutWeek.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['data'] = json.dumps(
            [
                {
                    'id': obj.id,
                    'total_sleep': obj.total_sleep,
                    'end_date': obj.end_date.isoformat(),
                    'bench_max': obj.bench_max
                }
                for obj in WorkoutWeek.objects.all()
            ]
        )
        return context

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password != confirmpassword:
            messages.error(request, 'Your username and/or password was not correct.')
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(request, 'Your account has been successfully created.')

        return redirect('authentication:index')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('authentication:index')
        else:
            messages.error(request, 'Your username and/or password was not correct.')
            return redirect('authentication:index')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, 'Logged out succesfully!')
    return redirect('authentication:index')