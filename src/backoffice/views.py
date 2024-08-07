from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib import messages



# this is the part of the website accessible only to admin
@login_required
def dashboard(request):
    

    context = {
        
    }

    return render(request, 'backoffice/backoffice_base.html', context)
