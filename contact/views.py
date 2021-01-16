from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.views.generic.base import View

from .models import Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from .decorators import allowed_users
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import generate_token
from django.contrib.sites.models import Site


# Create your views here.
# @allowed_users(allowed_roles=['admin'])
def contact(request):
    if request.method == 'POST':
        contact = Contact()
        contact.firstname = request.POST.get('firstname')
        contact.lastname = request.POST.get('lastname')
        contact.phone = request.POST.get('phone')
        contact.email = request.POST.get('email')
        contact.message = request.POST.get('message')
        contact.save()
        return redirect("home")
    else:
        return render(request, 'contact.html', {})


def message(request):
    return render(request, 'message.html', {})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Username or Password is Incorrecet")
    return render(request, 'account/login.html', {})


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()
            site = Site(domain="127.0.0.1:8000", name="My Blog site")
            # making email activation
            current_site = get_current_site(request)
            print("Current Site is : ",current_site)
            email_subject = "Activate Your Account"
            message = render_to_string("account/activate.html",
                                       {
                                           'user': instance,
                                           'domain': current_site.domain,
                                           'uid': instance.id,
                                           'token': generate_token.make_token(instance)

                                       }
                                       )
            to_email = form.cleaned_data.get('email')
            print("Email To : ", to_email)
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(email_subject, message, from_email, to_list, fail_silently=True)
            return render(request,"account/confirmation.html",{
                'name':form.cleaned_data.get('username'),
            })
            # email_message = EmailMessage(
            #     email_subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [instance.email]
            # )
            # email_message.send(fail_silently=True)
            # end of email activation

            username = form.cleaned_data.get('username')
            messages.success(request,
                             "An account has been created for " + username + ". Please login for having better experience.")
            return redirect('login')

    context = {
        'form': form,

    }
    return render(request, 'account/register.html', context)


def logoutUser(request):
    messages.success(request, "You are successfully logged out. Thanks for being with me")
    logout(request)

    return redirect('login')


class ActivateAccountView(View):
    def get(self,request,uid,token):
        try:
            user = get_object_or_404(User,pk=uid)

        except:
            raise HttpResponse("No user Found")

        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Account activated Succesfully.Please Login to experience the full support.')
            return redirect('login')
        else:
            return HttpResponse("<h1>Token is Invalid. Try to Register Again</h1>")



        # try:
        #     uid = force_text(urlsafe_base64_decode(uid))
        #     user = User.objects.get(pk=uid)
        # except Exception as identifier:
        #     user = None
        #
        # if user is not None and generate_token.check_token(user,token):
        #     user.is_active = True
        #     user.save()
        #     messages.add_message(request,messages.INFO,'Account activated Succesfully')
        #     return redirect('login')
        #
        # return render(request,'account/activate_failed.html',status=401)
