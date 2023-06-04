from django.shortcuts import render, redirect
from .models import ShippingDetails
from .forms import ShippingDetailsForm
from django.db.models import Q
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import random
# Create your views here.

def home(request):
    context = {}
    return render(request, 'home.html', context)

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if query:
            results = ShippingDetails.objects.filter(Q(tracking_number__icontains=query))
        else:
            results = ShippingDetails.objects.none()

        context = {
            'query': query,
            'results': results,
        }

        return render(request, 'track.html', context)
    else:
        return render(request, 'track.html')


def register(request):
    form_name = UserForm()
    if request.method =="POST":
        form_name = UserForm(request.POST)
        if form_name.is_valid():
            form_name.save()
            messages.success(request, "You have registered successfully")
            return redirect('signin')
        else:
            messages.error(request, 'Password not secure') 
            return redirect('register')
    else:
        context = {'form_name':form_name}
        
    return render(request, 'register.html', context )


def signin(request):
    if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('shipwithus')
            else:
                messages.info(request, 'Invalid username or password.. Please try again.')
                return redirect('signin')
    form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'signin.html', context)


@login_required(login_url='signin')
def shipwithus(request):
    form = ShippingDetailsForm()
    if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)
    if form.is_valid():
            shipping_form = form.save(commit=False)
            shipping_form.username = request.user
            shipping_form.save()
            form = ShippingDetailsForm()
            
    return render (request, 'shipwithus.html', {'form': form})

      
     
    


