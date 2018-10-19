from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve, Resolver404

# Create your views here.
from registration.forms import RegisterForm


def ajaxlogin(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")

    ret_data = {
        "logged_in": False
    }

    q_set = User.objects.filter(username=username)

    if len(q_set) > 0:
        user = q_set[0]
        if user.check_password(password):
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            ret_data["logged_in"] = True

    return ret_data


def ajaxgoogleauth(request):
    ret_data = {

    }
    return ret_data


def ajaxauth(request):
    auth_option = request.POST.get("auth_option", True)
    # auth_option = 1 : normal login
    #               2 : normal signup
    #               3 : google login
    #               4 : github login

    if auth_option == 1:
        ret_data = ajaxlogin(request)
        return JsonResponse(ret_data)

    elif auth_option == 3:
        ret_data = ajaxgoogleauth(request)
        return JsonResponse(ret_data)


def register(request):
    if request.method == "POST":
        registerform = RegisterForm(request.POST)
        next_page = request.POST.get("next_page", "")


        if registerform.is_valid():
            user = User.objects.create_user(username=registerform.cleaned_data["username"],
                                            email=registerform.cleaned_data["email"],
                                            password=registerform.cleaned_data["password"]
                                            )

            user.first_name = registerform.cleaned_data["first_name"]
            user.last_name = registerform.cleaned_data["last_name"]

            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            try:
                url_match = resolve(next_page)
                return redirect(next_page)
            except Resolver404:
                return redirect('home')

        else:
            return render(request, "registration/register.html", {
                "register_form": registerform,
                "next_page": next_page
            })

    else:
        registerform = RegisterForm()
        return render(request, "registration/register.html", {
            "register_form": registerform,
            "next_page": request.GET.get("next", "")
        })


def disqus(request):
    return render(request, 'registration/disqustrial.html')