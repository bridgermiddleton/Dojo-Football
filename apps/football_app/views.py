from django.shortcuts import render, redirect
import bcrypt

def loginpage(request):
    return render(request, "football_app/loginpage.html")


def registerpage(request):
    return render(request, "football_app/registerpage.html")

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            pass
    else:
        return redirect("/")

def register(request):
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash)
    request.session['userid'] = user.id
    pass

def logout(request):
   if 'userid' in request.session:
       del request.session['userid']
   return redirect("/")

def home(request):
    return render(request, "football_app/user_home.html")
