from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from .utils import yt_title, yt_subtitle, generateContent
from .models import Blog


# Create your views here.


def index(request):
    return render(request, "index.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect ("/")    
        return HttpResponse("Invalid credentials")

    return render(request, "signin.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        return redirect ("/")

    return render(request, "signup.html")


def signout(request):
    logout(request)
    return redirect("/")



@login_required(login_url="signin")
@csrf_exempt
def generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    try:
        print("It enter")
        data = json.loads(request.body)
        yt_link = data['url']
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid data sent"}, status=400)
    
    print(data)
    title = yt_title(yt_link)
    print(title)
    if title is None:
        return JsonResponse({"error": "Invalid YouTube link"}, status=400)
    print('enter transcript')
    transcript = yt_subtitle(yt_link)
    if transcript is None:
        return JsonResponse({"error": "Failed to generate transcript"}, status=500)
    print(transcript)
    print('enter content')    
    content = generateContent(transcript)
    if content is None:
        return JsonResponse({"error": "Failed to generate content"}, status=500)
    print(content)


    blog = Blog.objects.create(
        user=request.user, 
        youtube_link=yt_link,
        youtube_title=title, 
        generated_content=content,
    )

    blog.save()
    return JsonResponse({"content": content, "title": title})



def about(request):
    return render(request, 'about.html')


def all_blog(request):
    return render(request, "all_blog.html")