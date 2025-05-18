from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def home_view(request):
    return render(request, 'core/home.html')

def about_view(request):
    return render(request, 'core/about.html')

def miscellaneous_view(request):
    return render(request, 'core/miscellaneous.html')

def specimen_papers_view(request):
    return render(request, 'core/specimen_papers.html')

def teacher_notes_view(request):
    return render(request, 'core/teacher_notes.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill out all fields.')
    return render(request, 'core/contact.html')
