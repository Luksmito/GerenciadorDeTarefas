#'get_object_or_404' busca o objeto no banco de dados
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
import datetime

def helloWorld(request):
    return HttpResponse("Hello World")

@login_required
def taskList(request):
    
    search = request.GET.get('search') #search é o name do elemento de busca no html
    filter = request.GET.get('filter')
    tasksDoneRecently = Task.objects.filter(done='done', updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    tasksDone = Task.objects.filter(done='done', user=request.user).count()
    tasksDoing = Task.objects.filter(done='doing', user=request.user).count()
    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user) 
    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)
    else:
        task_list = Task.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(task_list, 5)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)

    return render(request, 'tasks/list.html', {'tasks': tasks, 'tasksrecently': tasksDoneRecently\
    ,'tasksdone': tasksDone, 'tasksdoing': tasksDoing})
    

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            #atribui o valor doing automaticamente a task pois ela acabou de ser criada
            task.done = 'doing'
            task.user = request.user
            task.save()
            return redirect('/')
    else:    
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.info(request, 'Tarefa deletada com sucesso')
    return redirect('/')

@login_required
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task) #formulario pré populado com a task
    if request.method == 'POST':
        
        form = TaskForm(request.POST)
        if form.is_valid():
            task.save()
            return redirect('/')
    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})
    
@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)

    if task.done == 'doing':
        task.done = 'done'
    else:
        task.done = 'doing'
    task.save()
    return redirect('/')
#o argumento 'name' é passado na url, pode ser visto o parametro na url
# no arquivo 'urls.py'
def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name': name})

