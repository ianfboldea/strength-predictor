import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.urls import reverse
import joblib
import numpy as np
import sklearn
from datetime import datetime, date, timedelta


from .models import WorkoutWeek

class IndexView(generic.ListView):
    template_name = 'authentication/index.html'
    context_object_name = 'workouts_list'

    def post(self, request):
        user = get_object_or_404(User, pk=int(request.POST.get('user')))
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
            user=user,
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
                    'end_date': obj.end_date.isoformat(),
                    'total_calories': obj.total_calories,
                    'total_sleep': obj.total_sleep,
                    'total_chest': obj.total_chest,
                    'total_shoulders': obj.total_shoulders,
                    'total_triceps': obj.total_triceps,
                    'total_protein': obj.total_protein,
                    'total_carbs': obj.total_carbs,
                    'bench_max': obj.bench_max,
                    'user': obj.user.id
                }
                for obj in WorkoutWeek.objects.all()
            ]
        )
        return context

class PredictionView(generic.ListView):
    template_name = 'authentication/predictions.html'
    context_object_name = 'workout_list'

    def get_queryset(self):
        return WorkoutWeek.objects.all()

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=int(request.POST.get('user')))
        total_calories = int(request.POST.get('total_calories'))
        total_sleep = int(request.POST.get('total_sleep'))
        total_chest = int(request.POST.get('total_chest'))
        total_shoulders = int(request.POST.get('total_shoulders'))
        total_triceps = int(request.POST.get('total_triceps'))
        total_protein = int(request.POST.get('total_protein'))
        total_carbs = int(request.POST.get('total_carbs'))
        bench_max = int(WorkoutWeek.objects.latest('end_date').bench_max)
        predict_weeks = int(request.POST.get('predict_weeks'))

        temp = [
            {
                'id': obj.id,
                'end_date': obj.end_date.isoformat(),
                'total_calories': obj.total_calories,
                'total_sleep': obj.total_sleep,
                'total_chest': obj.total_chest,
                'total_shoulders': obj.total_shoulders,
                'total_triceps': obj.total_triceps,
                'total_protein': obj.total_protein,
                'total_carbs': obj.total_carbs,
                'bench_max': obj.bench_max,
                'user': obj.user.id
            }
            for obj in WorkoutWeek.objects.all()
        ]

        model_clone = joblib.load('authentication/my_model.pkl')
        temp_bench_max = bench_max

        predictions = []

        for i in range(1, int(predict_weeks)+1):
            input_data = (total_calories,total_sleep,total_chest,total_shoulders,total_triceps,
            total_protein,total_carbs,temp_bench_max)
            input_data_as_numpy_array = np.asarray(input_data)
            input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
            prediction = model_clone.predict(input_data_reshaped)
            if prediction[0]==1:
                temp_bench_max += 5
            temp.append({
                'id': 0,
                'end_date': (WorkoutWeek.objects.latest('end_date').end_date + timedelta(weeks=i)).isoformat(),
                'total_calories': total_calories,
                'total_sleep': total_sleep,
                'total_chest': total_chest,
                'total_shoulders': total_shoulders,
                'total_triceps': total_triceps,
                'total_protein': total_protein,
                'total_carbs': total_carbs,
                'bench_max': temp_bench_max,
                'user': user.id
            })

        data = json.dumps(temp)

        return render(request, 'authentication/predictions.html', {'data': data})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['data'] = json.dumps(
            [
                {
                    'id': obj.id,
                    'end_date': obj.end_date.isoformat(),
                    'total_calories': obj.total_calories,
                    'total_sleep': obj.total_sleep,
                    'total_chest': obj.total_chest,
                    'total_shoulders': obj.total_shoulders,
                    'total_triceps': obj.total_triceps,
                    'total_protein': obj.total_protein,
                    'total_carbs': obj.total_carbs,
                    'bench_max': obj.bench_max,
                    'user': obj.user.id
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
            print(password, confirmpassword)
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