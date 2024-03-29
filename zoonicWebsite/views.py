from django.shortcuts import render, redirect
from users.models import Registro, Teacher
from .processing import get_average
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Email modules
from django.core.mail import send_mail
# Access env
from dotenv import load_dotenv
# Forms
from . import forms

# -- DASHBOARD
def index(request):
    if request.user.is_authenticated:
        return redirect("zoonicWebsite:general", 1)
    else:
        return redirect("zoonicWebsite:log_in")

def general(request, difficulty):
    if request.user.is_authenticated:
        all_logs = Registro.objects.filter(difficulty = difficulty)
        context = get_average(all_logs, difficulty)
        return render(request, 'zoonicWebsite/average.html', context)
    else:
        return redirect("zoonicWebsite:log_in")

def classroomA(request, difficulty):
    if request.user.is_authenticated:
        all_logs = Registro.objects.filter(difficulty = difficulty, classroom = 'A')
        context = get_average(all_logs, difficulty, 'A')
        return render(request, 'zoonicWebsite/average.html', context)
    else:
        return redirect("zoonicWebsite:log_in")

def classroomB(request, difficulty):
    if request.user.is_authenticated:
        all_logs = Registro.objects.filter(difficulty = difficulty, classroom = 'B')
        context = get_average(all_logs, difficulty, 'B')
        return render(request, 'zoonicWebsite/average.html', context)
    else:
        return redirect("zoonicWebsite:log_in")

def dashboard(request, difficulty, classroom, role_number):
    if request.user.is_authenticated:
        # Calling the Api
        response = requests.get(f'http://localhost:8000/api/view-logs-student/{difficulty}/{classroom}/{role_number}')
        response = response.json()  
        logs = response['logs']
        context = {'total_logs':0, 'last_level':0, 'best_grade':0, 'best_time':0,
                   'classroom': classroom, 'role_number': role_number,
                   'level_logs': {'1':[], '2':[], '3':[]}, 'difficulty': difficulty}

        foundTeachers = Teacher.objects.filter(classroom = context['classroom'])
        profesoresText = ''
        if(len(foundTeachers) == 0):
            profesoresText = 'Sin profesor asignado'
        elif(len(foundTeachers) == 1):
            profesoresText = foundTeachers[0].user
        else:
            for teacher in foundTeachers:
                profesoresText += str(teacher.user) + ', '

            profesoresText = profesoresText[:-2]

        context['profesores'] = profesoresText
        
        # Getting all the logs
        context['total_logs'] = len(logs)

        # Getting the best_grade, best_time, last_level and level_logs
        best_grade = 0
        best_time = float('inf')
        last_level = 0

        for log in logs:
            grade = log['grade']
            time = log['time']
            level = log['level']

            if(grade > best_grade):
                best_grade = grade

            if(time < best_time):
                best_time = time

            if(level > last_level):
                last_level = level
            
            context['level_logs'][f'{level}'].append({
                'grade': grade,
                'time': time,
                'date': log['date'],
            })

        context['best_grade'] = best_grade
        context['best_time'] = best_time
        context['last_level'] = last_level

        return render(request, 'zoonicWebsite/studentDashboard.html', context)
    else:
        return redirect("zoonicWebsite:log_in")

def notfound(request):
    if request.user.is_authenticated:
        return render(request, 'zoonicWebsite/notfound.html')
    else:
        return redirect("zoonicWebsite:log_in")

def log_in(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if(user.is_staff):
                return redirect('zoonicWebsite:read')
            else:
                return redirect('zoonicWebsite:general', 1)
        else:
            messages.error(request,("Usuario o password incorrectos."))
            return redirect("zoonicWebsite:log_in")
        
    return render(request, 'zoonicWebsite/login.html')

def log_out(request):
    logout(request)
    return redirect('zoonicWebsite:landing')

def readUsers(request):
    if request.user.is_authenticated & request.user.is_staff:
        all_logs = User.objects.filter()
        context = {'users': list(all_logs)}
        return render(request, 'zoonicWebsite/readUsers.html', context)
    else:
        return redirect("zoonicWebsite:log_in")

def updateDeleteUser(request, username):
    if request.user.is_authenticated & request.user.is_staff:
        user = User.objects.filter(username = username)
        user = user[0]
        context = {'username': user.username, 'email': user.email, 
                'first_name': user.first_name, 'last_name': user.last_name,
                'is_staff': int(user.is_staff)}

        # Looking for teacher attributes
        if(not user.is_staff):
            teacher = Teacher.objects.filter(user = user.id)
            if(len(teacher) == 0):
                context['classroom'] = ''
            else:
                teacher = teacher[0]
                context['classroom'] = teacher.classroom
        
        return render(request, 'zoonicWebsite/updateDeleteUser.html', context)
    else:
        return redirect("zoonicWebsite:log_in")

def createUser(request):
    if request.user.is_authenticated & request.user.is_staff:
        return render(request, 'zoonicWebsite/createUser.html')
    else:
        return redirect("zoonicWebsite:log_in")

def download(request):
    return render(request, 'zoonicWebsite/download.html')

def landing(request):
    return render(request, 'zoonicWebsite/landing.html')

def license(request):
    return render(request, 'zoonicWebsite/license.html')