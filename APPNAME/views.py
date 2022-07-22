
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from mechanize import Browser
import favicon
from .models import Password

br = Browser()
br.set_handle_robots(False)
fernet = Fernet(settings.KEY.encode())
LOGIN_REDIRECT_URL= '/logger'

def outlet(request):
    return render(request,"APPNAME/outlet.html")

def otp(request):
    if "confirm" in request.POST:
            one = request.POST.get("one")
            two = request.POST.get("two")
            three = request.POST.get("three")
            four = request.POST.get("four")
            five = request.POST.get("five")
            six = request.POST.get("six")
            input_code = one+two+three+four+five+six
            user_t = request.POST.get("user")
            if input_code != global_code:
                msg = f"{input_code} is wrong!"
                return render(request,"APPNAME/otp.html",{"nuser":user_t, "message":msg})
    
            else:
                login(request,User.objects.get(username=user_t))
                return redirect(home)

    else:
        return render(request,"APPNAME/outlet.html")
def logger(request):
    if 'login-form' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            new_login = authenticate(request, username=username, password=password)
            if new_login is None:
                logout(request)
                return render(request,"APPNAME/login.html",{"message":'Login failed! Make sure you are using the right credentials',"flag":1 })
            else:
                code = str(random.randint(100000, 999999))
                global global_code
                global_code = code
                send_mail(
                    "Key Knots : confirm email",
                    f"Your verification code is {code}.",
                    settings.EMAIL_HOST_USER,
                    [new_login.email],
                    fail_silently=False,
                )
                return render(request, "APPNAME/otp.html", {
                    "code":code, 
                    "nuser":username,
                })
 
    else:
     return render(request,"APPNAME/login.html",{"message":'Login to Key Knots', "flag":0})

def signer(request):
    if request.method == "POST":
        if "signup-form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            #if password are not identical
            if password != password2:
                return render(request,"APPNAME/signup.html",{"message":'Password and Confirmed password are not matching',"flag":1})
                
            #if username exists
            elif User.objects.filter(username=username).exists():
               return render(request,"APPNAME/signup.html",{"message":'this username already exist , plz try another',"flag":1})

            #if email exists
            elif User.objects.filter(email=email).exists():
                return render(request,"APPNAME/signup.html",{"message":'this email already exist , plz try another',"flag":1})

            else:
                User.objects.create_user(username, email, password)
                new_user = authenticate(request, username=username, password=password2)
                if new_user is not None:
                    login(request, new_user)
                    msg = f"{username}. Thanks for subscribing. this is your vault"
                    messages.success(request, msg)
                    return redirect(home)
    else:    
        return render(request,"APPNAME/signup.html",{"message":'hello new friend',"flag":0})


@login_required(login_url=LOGIN_REDIRECT_URL)
def home(request):
    context = {}
    if request.user.is_authenticated:
        passwords = Password.objects.all().filter(user=request.user)
        map_={}
        count=0
        for password in passwords:
            password.email = fernet.decrypt(password.email.encode()).decode()
            password.password = fernet.decrypt(password.password.encode()).decode()
            s = password.password
            if s not in map_: 
                map_[s]=1

            else:
                map_[s]+=1

        for key in map_:
            if(map_[key]>1):
                count+=1

        map_.clear()        
        context = {
            "passwords":passwords,
            "duplicate":count,
            "curguy":request.user.username
        }   

        return render(request, "APPNAME/home.html", context)

    else:
        return render(request,"APPNAME/outlet.html")    

def update(request):
    if 'update' in request.POST:
        to_update = request.POST.get("password-id")
        old_data=Password.objects.get(id=to_update)
        old_mail = fernet.decrypt(old_data.email.encode()).decode()
        old_pass =fernet.decrypt(old_data.password.encode()).decode()
        site = old_data.name
        icon = old_data.logo
        Password.objects.get(id=to_update).delete()
        guy = request.POST.get("user")
        return render(request,"APPNAME/update.html",{"icon":icon,"site":site,"oldmail":old_mail,"oldpass":old_pass,"curusr":guy})

    elif 'changer' in request.POST:
        nguy = request.POST.get("user")
        login(request,User.objects.get(username=nguy))
        nmail=request.POST.get("newmail")
        npass=request.POST.get("newpass")
        nsite = request.POST.get("site")
        nicon = request.POST.get("ikon")
        encrypted_email = fernet.encrypt(nmail.encode())
        encrypted_password = fernet.encrypt(npass.encode())
        new_password = Password.objects.create(
                user=request.user,
                name=nsite,
                logo=nicon,
                email=encrypted_email.decode(),
                password=encrypted_password.decode(),
            )

        return redirect(home)

def adder(request):
    if "add-password" in request.POST:
            ourguy = request.POST.get("user")
            login(request,User.objects.get(username=ourguy))
            url = request.POST.get("url")
            email = request.POST.get("email")
            password = request.POST.get("password")
            #ecrypt data
            encrypted_email = fernet.encrypt(email.encode())
            encrypted_password = fernet.encrypt(password.encode())
            #get title of the website
            try:
                br.open(url)
                title = br.title()
            except:
                title = url

            s =""

            for i in title:
                if i !=" ":
                      s+=i
                else:
                     break
    
            temp = title[:8]

            if temp=="https://":
                        s=s[8:]

            title = s
            #get the logo's URL
            try:
                icon = favicon.get(url)[0].url
            except:
                icon = "https://cdn-icons-png.flaticon.com/512/3170/3170748.png"
            #Save data in database
            new_password = Password.objects.create(
                user=request.user,
                name=title,
                logo=icon,
                email=encrypted_email.decode(),
                password=encrypted_password.decode(),
            )
            msg = f"{title} added successfully."
            messages.success(request, msg)
            return redirect(home)

def delete(request):    
    if "delete" in request.POST:
        guy = request.POST.get("user")
        login(request,User.objects.get(username=guy))     
        to_delete = request.POST.get("password-id")
        msg = f"{Password.objects.get(id=to_delete).name} deleted."
        Password.objects.get(id=to_delete).delete()
        messages.success(request, msg)
        return redirect(home)

def logout(request):
    if "logout" in request.POST:
        guy = request.POST.get("user")
        return render(request,"APPNAME/outlet.html")


def mailer(request):
     if "mailed" in request.POST:
        clientmail = request.POST.get("email")
        sms = request.POST.get("message")
        clientname = request.POST.get("name")
        send_mail(
                    "Key Knots : user query",
                    f"from : {clientmail} ,client : {clientname}. query: "+sms,
                    settings.EMAIL_HOST_USER,
                    ["ford-fulkerson@outlook.com"],
                    fail_silently=False,
                )    
        return render(request,"APPNAME/outlet.html",{"mess":"we have received your query Thank you!"})
