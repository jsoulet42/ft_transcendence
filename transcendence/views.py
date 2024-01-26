from django.shortcuts import render

def view_403(request, exception):
    return render(request, '403.html')

def view_404(request, exception):
    return render(request, '404.html')

def view_500(request):
    return render(request, '500.html')