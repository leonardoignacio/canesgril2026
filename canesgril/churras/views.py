from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def churrasco(request):
    return render(request, 'churrasco.html')
    
