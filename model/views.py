from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import IceCream
from .forms import IceCreamForm

class IceCreamListView(View):
    def get(self, request):
        ice_creams = IceCream.objects.all()
        return render(request, 'model/icecream_list.html', {'ice_creams': ice_creams})

class IceCreamDetailView(View):
    def get(self, request, ice_cream_id):
        ice_cream = get_object_or_404(IceCream, id=ice_cream_id)
        return render(request, 'model/icecream_detail.html', {'ice_cream': ice_cream})

class IceCreamCreateView(View):
    def get(self, request):
        form = IceCreamForm()
        return render(request, 'model/icecream_form.html', {'form': form})

    def post(self, request):
        form = IceCreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ice_cream_list')
        return render(request, 'model/icecream_form.html', {'form': form})

class IceCreamUpdateView(View):
    def get(self, request, ice_cream_id):
        ice_cream = get_object_or_404(IceCream, id=ice_cream_id)
        form = IceCreamForm(instance=ice_cream)
        return render(request, 'model/icecream_form.html', {'form': form})

    def post(self, request, ice_cream_id):
        ice_cream = get_object_or_404(IceCream, id=ice_cream_id)
        form = IceCreamForm(request.POST, instance=ice_cream)
        if form.is_valid():
            form.save()
            return redirect('icecream_list')
        return render(request, 'model/icecream_form.html', {'form': form})

class IceCreamDeleteView(View):
    def get(self, request, ice_cream_id):
        ice_cream = get_object_or_404(IceCream, id=ice_cream_id)
        ice_cream.delete()
        return redirect('icecream_list.html')
