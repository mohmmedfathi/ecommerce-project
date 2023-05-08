from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib import auth
def register(request):
    
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
                
            user = Account.objects.create_user(
                first_name= first_name,
                last_name= last_name,
                email= email,
                username= email,
                password=password
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registeration Successful .')
            return redirect("register")
    else :   
        form = RegistrationForm()
        
    context = {
        'form' : form,
        
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        
        if user is not None:
            auth.login(request,user)
            # messages.success(request,'You are logged in Successfuly')
            return redirect('home')
        
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    context = {}
    return render(request,'accounts/login.html',context)

def logout(request):
    context = {}
    return render(request,'accounts/logout.html',context)
