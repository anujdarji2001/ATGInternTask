from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_control

# Create your views here.

def home(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    return render(request, 'app/index.html',{'usr':user, 'user_type':user_type})

def blogs(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    blogs = BlogForm.objects.filter(draft = False)
    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    return render(request, 'app/blogs.html',{'blogs':blogs,'user_type':user_type})


def draft(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    blogs = BlogForm.objects.filter(draft = True)
    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    return render(request, 'app/draft.html',{'blogs':blogs,'user_type':user_type})


def editdraft(request,id):
    if request.session.get('vendor') == None:
        return redirect('login')

    blogcat = ['Mental Health','Heart Disease','Covid19','Immunization']

    blog = BlogForm.objects.get(id=id)
    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type


    if request.method == 'POST':
        blog.titleofblog = request.POST['titleofblog']
        blog.summaryofblog = request.POST['summaryofblog']
        blog.contentofblog = request.POST['contentofblog']
        # blog.blogpic = request.FILES['blogpic']
        blog.categoryofblog = request.POST['categoryofblog']

        if request.POST.get('draft',''):
                draft = True
        else:
            draft = False

        blog.draft = draft
        blog.save()

        if draft == False:
            msg = 'Your Blog is Successfully Created.'
            blogs = BlogForm.objects.all()
            return render(request, 'app/blogs.html',{'msg':msg,'blogs':blogs,'user_type':user_type})
        else:
            msg = 'Your Blog is Drafted.'
            blogs = BlogForm.objects.filter(draft = True)
            return render(request, 'app/draft.html',{'msg':msg,'blogs':blogs,'user_type':user_type})

    return render(request, 'app/editdraft.html',{'blog':blog,'user_type':user_type, 'blogcat':blogcat})

def deleteblog(request,id):
    if request.session.get('vendor') == None:
        return redirect('login')

    blog = BlogForm.objects.get(id=id)
    blog.delete()

    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    blogs = BlogForm.objects.filter(user=user)
    user_type = user.user_type

    return render(request, 'app/myblog.html',{'blogs':blogs,'user_type':user_type})

def myblog(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    blogs = BlogForm.objects.filter(user=user)
    user_type = user.user_type

    return render(request, 'app/myblog.html',{'blogs':blogs,'user_type':user_type})

def createblog(request):
    if request.session.get('vendor') == None:
        return redirect('login')

    cuser = request.session.get('vendor_email')
    user = CustomUser.objects.get(email=cuser)
    user_type = user.user_type

    if request.method == 'POST':
        titleofblog = request.POST['titleofblog']
        summaryofblog = request.POST['summaryofblog']
        contentofblog = request.POST['contentofblog']
        blogpic = request.FILES['blogpic']
        categoryofblog = request.POST['categoryofblog']

        print(categoryofblog)

        cuser = request.session.get('vendor_email')
        user = CustomUser.objects.get(email=cuser)

        if request.POST.get('draft',''):
                draft = True
        else:
            draft = False

        BlogForm(user=user,titleofblog=titleofblog, summaryofblog=summaryofblog,  contentofblog=contentofblog, categoryofblog = categoryofblog,
                blogpic=blogpic,draft=draft).save()


        if draft == False:
            msg = 'Your Blog is Successfully Created.'
            blogs = BlogForm.objects.all()
            return render(request, 'app/blogs.html',{'msg':msg,'blogs':blogs,'user_type':user_type})
        else:
            msg = 'Your Blog is Drafted.'
            blogs = BlogForm.objects.filter(draft = True)
            return render(request, 'app/draft.html',{'msg':msg,'blogs':blogs,'user_type':user_type})


    return render(request, 'app/createblog.html',{'user_type':user_type})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):

    if request.session.get('vendor') != None:
        return redirect('home')

    department = ['patient', 'doctor']

    if request.method == 'POST':
        dname = request.POST['dname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        propic = request.FILES['propic']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if CustomUser.objects.filter(username=username):
            msg = 'Username already exist please try some other Username'
            return render(request,'app/signup.html',{'department':department,'msg':msg})

        if CustomUser.objects.filter(email=email):
            msg = 'Email alredy registred'
            return render(request,'app/signup.html',{'department':department,'msg':msg})
        
        if (password == confirm_password):
            usr = CustomUser.objects.create_user(user_type=dname,first_name=fname,last_name=lname,propic= propic,
                                username=username,email=email,password=password,address=address,
                                city=city,state=state,pincode=pincode)
            usr.is_active = True
            usr.is_staff = True
            usr.save()
            return redirect('login')
            
        else:
            msg = "Password are not matched!!!"
            return render(request,'app/signup.html',{'department':department,'msg':msg})

    return render(request,'app/signup.html',{'department':department})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):

    department = ['patient', 'doctor']

    if request.session.get('vendor') != None:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']
        dname = request.POST['dname']

        print(email,pwd)
        usr = authenticate(email=email,password=pwd)
        print(usr)
        if usr:
            usr = CustomUser.objects.get(email=email)
            if usr.user_type == dname :
                if (usr.is_staff == True):
                    vendor = {'vendor_name':usr.username,'vendor_email':usr.email}
                    request.session['vendor'] = vendor
                    request.session['vendor_email'] = usr.email
                    return redirect('home')
                else:                
                    return render(request,'app/login.html',{'department':department})
            else:
                msg = "Incorrect Details!!!"
                return render(request,'app/login.html',{'msg':msg,'department':department})
        else:
            msg = "Incorrect Email or Password!!!"
            return render(request,'app/login.html',{'msg':msg,'department':department})
    
    return render(request,'app/login.html',{'department':department})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if (request.session.get('vendor') != None):
        request.session.delete()
        return redirect('login')
    else:
        return redirect('login')
