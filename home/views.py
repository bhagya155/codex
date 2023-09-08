from django.shortcuts import render,HttpResponse , redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth import authenticate,login, logout 
from django.contrib.auth.models import User
# pages.
def home(request):
    allPost = Post.objects.all()
    context = {'allpost':allPost}
    return render(request,"home/home.html",context)
    
def about(request):
    return render(request,"home/about.html")
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        
        if len(name) < 2 or len(email) < 3 or len(phone) < 9 or len(content) < 3 :
            messages.warning(request, "Please Enter Correct data")
        else:
            contact = Contact(name=name, email=email,phone=phone,content=content)
            contact.save()
            messages.success(request, "Your message has been sent")

    return render(request,"home/contact.html")

def search(request):
    query = request.GET['query']
    if len(query) > 67:
        allPost = []
    else:
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostcontent = Post.objects.filter(content__icontains=query)
        allPost = allPostTitle.union(allPostcontent)

    if len(allPost) == 0:
        messages.warning(request, "try another keywords")

    context = {'allpost':allPost,'query':query}
    return render(request,"home/search.html",context)

# authentication API's
def handleSignup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname= request.POST['lastname']
        username= request.POST['username']
        email= request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        print(len(username))
        if len(username)<10:
            messages.warning(request, "username should be grater than 10 charcters")
            
        elif password1 != password2:
            messages.warning(request, "passwords should be equal")
            
        else:
            myuser = User.objects.create_user(username, email, password1)
            myuser.first_name = firstname
            myuser.last_name = lastname
            myuser.save()
            messages.success(request, "Your CodeX Account is created Successfully")
            
        return redirect('home')
    else:
        return HttpResponse("404 not found")
    
def handlelogin(request):
    if request.method == "POST":
        username= request.POST['loginusername']
        password= request.POST['password']
        user = authenticate(username=username,password=password)
        if user != None :
            login(request, user)
            messages.success(request, "Successfully Login")
            return redirect ('home')
        else:
            messages.warning(request, "Invalid Credential ")
            return redirect ('home')

    return HttpResponse("login")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully Loged out")
    return redirect('home')
    