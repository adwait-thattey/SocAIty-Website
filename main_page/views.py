from django.shortcuts import render, redirect

# Create your views here.
from main_page.models import Progress
from .forms import ContactUsForm


def index(request):
    progress = Progress.objects.all()[0]

    if request.method == "POST":
        contact_us_form = ContactUsForm(request.POST)
        if contact_us_form.is_valid():
            contact_us_form.save()
            return render(request, "main_page/message.html",
                          {"message": "Thank You for Contacting Us. We will get back to you shortly"})
    else:
        contact_us_form = ContactUsForm()
    return render(request, 'main_page/index.html', {"progress": progress, "contact_us_form": contact_us_form})


def contact(request):
    if request.method == "POST":
        pass
    else:
        return redirect('home')
