from django.shortcuts import render, redirect
from .models import ShippingDetails
from .forms import ShippingDetailsForm
from django.db.models import Q

# Create your views here.

def home(request):
    context = {}
    return render(request, 'home.html', context)

# def track(request):
#     if request.method == 'POST':
      
#             searched = request.POST['searched']
       
#             results = ShippingDetails.objects.filter(tracking_number__contains = searched)
            
#             return render(request, 'track.html', {'searched': searched, 'results': results} )

#     else:
#         return render(request, 'track.html')




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


def newshipping(request):
    
     form = ShippingDetailsForm()
     if request.method == 'POST':
        form = ShippingDetailsForm(request.POST)
     if form.is_valid():
            form.save()
            return redirect('home')    
     return render (request, 'contact.html', {'form': form})
    
