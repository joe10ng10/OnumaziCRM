from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import AddRecordForm

def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There was an Error Logging In, Please Try Again!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})



def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')



def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    
    else:
        messages.success(request, "You must be logged in to view that page..")
        return redirect('home')
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully..")
        return redirect('home')

    else:
        messages.success(request, "You Must Be Logged In To Do That..")
        return redirect('home')   
    
def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home') 
        return render(request, 'add_record.html', {'form':form})   
    
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def edit_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'edit_record.html', {'form':form})
    
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
        