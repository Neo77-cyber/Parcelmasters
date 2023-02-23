from django.shortcuts import render, redirect
from .models import ShippingDetails
from .forms import ShippingDetailsForm

# Create your views here.

def home(request):
    context = {}
    return render(request, 'home.html', context)

def track(request):
    if request.method == 'POST':
      
            searched = request.POST['searched']
       
            results = ShippingDetails.objects.filter(tracking_number__contains = searched)
            
            return render(request, 'track.html', {'searched': searched, 'results': results} )

    else:
        return render(request, 'track.html')

def newshipping(request):
    
     form = ShippingDetailsForm()
     if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)
     if form.is_valid():
            form.save()
            return redirect('home')    
     return render (request, 'contact.html', {'form': form})
    
