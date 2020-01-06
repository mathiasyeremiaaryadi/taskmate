from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    
    content = {'welcome_text': 'Welcome To The Home Page'}
    
    return render(request, 'index.html', content)

# Apply restriction login
@login_required
def todolist(request):
    
    # Check the request method
    # If post then add data, else show data
    if request.method == "POST":
        
        # Process the form
        form = TaskForm(request.POST or None)
        
        # Validation form
        if form.is_valid():
            
            # Save the task
            instance = form.save(commit = False)
            instance.manage = request.user
            instance.save()
        
        # FLash message
        messages.success(request, ("New task added !"))
        
        return redirect('todolist')
        
    else:
        
        # Fetch data from model
        all_tasks = TaskList.objects.filter(manage = request.user)
        
        # Pagination: show 10 data per page
        paginator = Paginator(all_tasks, 10)
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)

        return render(request, 'todolist.html', {'all_tasks': all_tasks})

# Apply restriction login
@login_required
# Delete task
def delete_task(request, task_id):
    
    # Get the one task to be delete with task_id
    task = TaskList.objects.get(pk = task_id)
    
    if task.manage == request.user:

        # Delete the task
        task.delete()

        # FLash message
        messages.success(request, ("Task deleted !"))
        
    else:
        
        messages.error(request, ("Access Restricted, You Are Not Allowed"))
        
    return redirect('todolist')

# Apply restriction login
@login_required
# Edit task
def edit_task(request, task_id):
    
    if request.method == "POST":
        
        task = TaskList.objects.get(pk = task_id)
                    
        # Update task
        form = TaskForm(request.POST or None, instance = task)       
        if form.is_valid():
            
            form.save()
        
        messages.success(request, ("Task edited !"))
        
        return redirect('todolist')
        
    else:
        
        task_object = TaskList.objects.get(pk = task_id)
        
        return render(request, 'edit.html', {'task_object': task_object})

# Apply restriction login
@login_required   
# Complete task
def complete_task(request, task_id):
    
    task = TaskList.objects.get(pk = task_id)
    
    if task.manage == request.user:
    
        task.done = True
        
        task.save()
        
        messages.success(request, ("Task is completed"))
    
    else:
        
        messages.error(request, ("Access Restricted, You Are Not Allowed"))

    
    return redirect('todolist')

# Apply restriction login
@login_required
# Pending task
def pending_task(request, task_id):
    
    task = TaskList.objects.get(pk = task_id)
    
    task.done = False
    
    task.save()
    
    messages.success(request, ("Task is pending"))
    
    return redirect('todolist')

def contact(request):
    
    content = {'contact_text': 'Welcome To The Contact Page'}
    
    return render(request, 'contact.html', content)

def about(request):
    
    content = {'about_text': 'Welcome To The About Page'}
    
    return render(request, 'about.html', content)


    
    

