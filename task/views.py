from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Task
from datetime import datetime
from django.contrib.auth import authenticate, login as login_, logout as logout_
from django.contrib.auth.decorators import login_required

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'tasks': Task.objects.filter(user_id = request.user.id),
        'user': request.user
    }
    return render(request, 'index.html', context)

def task(request, task_name):
    task = Task.objects.get(name=task_name)
    deta_time_str, label_type = task.str_type()
    context = {'task': task, "delta_time": deta_time_str, 'label_type':label_type}
    return render(request, 'task.html', context)


def login(request):
    if not ('email' in request.POST and 'password' in request.POST):
        return render(request, 'login.html', {'invalid': False})

    user = authenticate(
        request,
        username=request.POST['email'],
        password=request.POST['password']
    )

    if user is not None:
        login_(request, user)
        return redirect('index')
    
    return render(request, 'login.html', {'invalid': True})

def register(request):
    if not ('email' in request.POST and 'password' in request.POST):
        return render(request, 'register.html')
    
    user = User.objects.create(
        username=request.POST['email'],
        password=request.POST['password']
    )
    user.save()
    login_(request, user)
    return redirect('index')
    

def logout(request):
    logout_(request)
    return redirect('index')

@login_required
def new_task(request):
    if not (
        'name' in request.POST and
        'deadline' in request.POST and
        'description' in request.POST
    ):
        return render(request, 'task_form.html')
    
    task = Task.objects.create(
        user_id=request.user.id,
        name=request.POST['name'],
        deadline=request.POST['deadline'],
        description=request.POST['description'],
    )
    task.save()
    return redirect('index')

@login_required
def edit_task(request, task_name):
    task = Task.objects.get(user_id=request.user.id, name=task_name)
    if not (
        'name' in request.POST and
        'deadline' in request.POST and
        'description' in request.POST
    ):
        context = {
            'name': task.name,
            'deadline': task.deadline,
            'description': task.description,
        }
        return render(request, 'task_form.html', context)
    
    task.name = request.POST['name']
    task.deadline = request.POST['deadline']
    task.description = request.POST['description']
    task.save()
    return redirect('index')

@login_required
def delete_task(request, task_name):
    task = Task.objects.get(user_id=request.user.id, name=task_name)
    task.delete()
    return redirect('index')