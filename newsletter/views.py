from django.shortcuts import render
from django.shortcuts import render

def index(request):
    """View for newsletter page"""
    return render(request, 'newsletter/index.html')
# Create your views here.
