from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def index(request):
    return render(request, "index.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect ("/")
    
        return HttpResponse("Invalid credentials")


    return render(request, "signin.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(username, "", password)
        user.save()
        login(request, user)
        return redirect ("/")

    return render(request, "signup.html")


def signout(request):
    logout(request)
    return redirect("/")