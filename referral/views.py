from .models import ReferralCode, ReferralRelationship
from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate  
from .forms import SignupForm, LoginForm
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_str, force_bytes
import secrets
from user.models import User

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            send_mail(  
                        mail_subject, message,settings.EMAIL_HOST_USER, [to_email]  
            )   
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(my_acc)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return redirect(login_view)  
    else:  
        return HttpResponse('Activation link is invalid!')  


def my_acc(request):
        # getting querry set with referral codes for user who make request
        queryset = ReferralCode.objects.filter(user=request.user)
        referrals = ReferralRelationship.objects.filter(employer=request.user.id)
        invited = ReferralRelationship.objects.filter(employee=request.user.id)
        context = {'data': queryset, 'referrals': referrals,
                   'invited': invited}
        return render(request, 'my_acc.html', context)


def create_token(request):
    # method for creating tokens
    
    token = secrets.token_urlsafe(20)
    ReferralCode(token=token, user=request.user).save()
    return redirect(my_acc)


def ratings(request):
    qs = User.objects.all()[:10]
    return render(request, 'ratings.html', {'users': qs})