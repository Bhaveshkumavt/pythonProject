# from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# from pylint.checkers.typecheck import _

from .models import Profile, Contact, Category
from .forms import ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login as login_process,logout,authenticate
from django.shortcuts import redirect,get_object_or_404
from django.template.loader import get_template
from django.contrib import messages
# Create your views here.

def home(request):
    # dat_key = request.session.items()
    return render(request, 'community/index.html')

def about_view(request):
    # dat_key = request.session.items()
    return render(request, 'community/about.html')

def signup_view(request):
    # sc_list = SubCategory.objects.all()
    if(request.method=='POST'):
        RF=RegistrationForm(request.POST)
        if(RF.is_valid()):
            RF.save(request)
            return HttpResponseRedirect(reverse('login'))
        else:
            print("some one is trying for register but failed", RF.errors)
            HttpResponse("invalid Data")
            HttpResponse(RF.errors)
    else:
        RF=RegistrationForm()
        print(RF)
        print('*****************8')
    return render(request,'signup.html',{'RF':RF})

class EmailAuthBackend:
    def authenticate(username,password,backend):
        try:
            user=User.objects.get(email=username)
            success=user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            pass
        return None

def user_login(request):
    session_var = request.session.items()
    if request.session.has_key('uname') and request.session.has_key('password'):
        uname = request.session['uname']
        pwd = request.session['password']
        a1 = EmailAuthBackend
        user = a1.authenticate(username=uname, password=pwd, backend='django.contrib.auth.backends.ModelBackend')
        login_process(request, user, 'django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        return user_login1(request)

def user_login1(request):
    uname=''
    pwd=''
    if(request.method=='POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        remind=request.POST.get('remember_me')
        print(remind)
        # u=User.objects.get(email=username)
        a1=EmailAuthBackend
        user = a1.authenticate(username=username,password=password,backend='django.contrib.auth.backends.ModelBackend')
        if user:
            if(user.is_active):
                login_process(request, user, 'django.contrib.auth.backends.ModelBackend')
                print("login have value **************************")
                if remind:
                    request.session['uname']=username
                    request.session['password']=password
                    print(request.session.items())
                    # request.session.set_expiry(None)
                    print("remind have value **************************")
                    # print(request.session.get_expiry_age())
                # return HttpResponseRedirect(reverse_lazy('index'))
                return home(request)
            else:
                return HttpResponse('user is not active')
        else:
            print('someone is trying to login with this username={} and password{}'.format(username,password))
            return HttpResponse('invalid username and password')

    return render(request,'login.html',{'uname':uname,'pwd':pwd})

@login_required
def user_logout(request):
    # sc_list = SubCategory.objects.all()
    data_key = request.session.items()
    uname = request.session.get('uname')
    pwd = request.session.get('password')
    logout(request)
    if uname and pwd:
        request.session['uname']=uname
        request.session['password']=pwd
    return render(request, 'community/index.html')

@login_required
def profile_view(request):
    p2=None
    global form_pic
    form_pic = None
    user=request.user
    pr=Profile.objects.filter(user=user)
    if request.method == 'POST':
        if pr.count() is not 0:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                print(form)
                form_pic = form.cleaned_data.get('picture')
            print("****************************")
            print(pr.count())
            p1=Profile.objects.get(user=user)
            n=request.POST.get('name')
            sta=request.POST.get('status')
            gen=request.POST.get('gender')
            add=request.POST.get('address')
            your_bio=request.POST.get('your_bio')
            your_facebook=request.POST.get('your_facebook')
            p=request.POST.get('picture')
            print(p)
            a=request.POST.get('age')
            if p1 is not None:
                p1.set_data(n,sta,gen,a,form_pic,your_facebook,your_bio,add)
                # p2=Profile.objects.get(user=user)
                # p1.Lname=lname
                messages.success(request,'profile update successfull',extra_tags='alert')
                return redirect('profile')
        else:
            p1 = Profile.objects.create(user=user)
            print(p1)
            n = request.POST.get('name')
            sta = request.POST.get('status')
            gen = request.POST.get('gender')
            add = request.POST.get('address')
            # p = request.POST.get('picture')
            your_bio = request.POST.get('your_bio')
            your_facebook = request.POST.get('your_facebook')
            a = request.POST.get('age')
            if p1 is not None:
                if p1.set_data(n,sta,gen,a,form_pic,your_facebook,your_bio,add)=='done':
                    pr=1
                    return HttpResponse("profile update successfully")
                else:
                    return HttpResponse("profile is not updated")
    if Profile.objects.filter(user=user).count() is not 0:
        print(Profile.objects.filter(user=user).count())
        p2=Profile.objects.get(user=user)
    form = ProfileForm()
    return render(request, 'community/profile.html', {'p2':p2, 'form':form})

@login_required
def contact_view(request):
    obj2=None
    global cf
    user = request.user
    print(user)
    print("****************8")
    # obj1 = Contact.objects.get(user=user)
    # print(obj1)
    cf = Contact.objects.filter(user=user)
    print(cf)
    if request.method == 'POST':
        if cf.count() is not 0:
            obj1 = Contact.objects.get(user=user)
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            msg = request.POST.get('msg')
            if obj1 is not None:
                obj1.set_data(f_name, l_name, email, mobile, msg)
                messages.success(request, 'Your contact request register successfully')
                cf = 1
                return home(request)
        else:
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            msg = request.POST.get('msg')
            obj1 = Contact.objects.create(user=user)
            print("************")
            print(obj1)
            if obj1 is not None:
                if obj1.set_data(f_name, l_name, email, mobile, msg) == 'done':
                    cf = 1
                    return home(request)
                else:
                    return HttpResponse("contact is not updated")


    if Contact.objects.filter(user=user).count() is not 0:
        print(Contact.objects.filter(user=user).count())
        obj2 = Contact.objects.filter(user=user)
    return render(request, 'community/contact.html', {'obj2':obj2})
