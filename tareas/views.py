from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .models import Tarea
from .forms import TareaForm
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def task (request):
    tareas=Tarea.objects.filter(user=request.user, completada_fecha__isnull =True)
    return render (request, 'task.html', {"tasks":tareas})
@login_required
def tasks_completed(request):
    tareas=Tarea.objects.filter(user=request.user, completada_fecha__isnull=False).order_by('-completada_fecha')
    return render(request, 'task.html', {"tasks": tareas})
@login_required
def create_task(request):
    if request.method=="GET":
        print ("entro a el metodo get")
        return render(request, 'create_task.html', {"form": TareaForm } )
        
    else:
        try:
            form =TareaForm(request.POST)
            print("entro al metodo post")
            new_task =form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print("ya guardo")
            return redirect('task')
        except ValueError:
            print("entro al mensaje de error")
            return render(request, "create_task.html",
            {"form": TareaForm, "error":"Error al crear tarea"} )
@login_required
def task_detail(request, task_id):
    print (task_id)
    print('estoy en detalle tarea')
    
    if request.method =='GET':
        print('estoy en el metodo get de task_detail')
        task=get_object_or_404(Tarea, pk= task_id, user=request.user)
        form =TareaForm(instance=task)
        return render(request, 'task_detail.html', {'task':task,'form':form})
    else:
        try:
            task = get_object_or_404(Tarea, pk=task_id, user=request.user )
            form= TareaForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request,'task_detail.html',{'task': task, 'form': form, 'error':'Error al intentar mostrar los datos'})
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Tarea, pk=task_id, user=request.user)
    if request.method =='POST':
        task.completada_fecha =timezone.now()
        task.save()
        return redirect('task')
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tarea, pk=task_id, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('task')



def home (request):
    return render(request, 'home.html')

def signup (request):
    if  request.method =="GET":
        return render(request, 'signup.html',
        {'form': UserCreationForm})
    else:
        if request.POST ['password1']==request.POST['password2']:
            
            try:
                usuario = User.objects.create_user(request.POST ['username'],
                password=request.POST['password1'])
                
                usuario.save()
                
                login(request, usuario)
    
                return redirect('task')
            except IntegrityError :
               return render(request, 'signup.html',
        {'form': UserCreationForm,
        'error':'Usuario existe'})
        return render(request, 'signup.html', {'form': UserCreationForm,
        'error':'Contrasena no coinciden'})
@login_required
def signout(request):
    logout (request)
    return redirect('home')

def signin(request):
    if request.method=='GET':
        print('en el metodo GET')
        print(request.GET)

        return render(request, 'signin.html',{
        'form': AuthenticationForm
        })
    else:
        print('en el post tenemos:')
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print("usuario o contrasena incorrectos")
            return render(request, 'signin.html',{
                'error': "Usuario o contraseña son incorrectos",
                'form': AuthenticationForm
        })
        login(request,user)
        return redirect('task')


