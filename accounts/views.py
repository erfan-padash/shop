
        response = api.sms_send(params)
        print(re
        response = api.sms_send(params)
        print(reimport datetime
from pytz import timezone
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
import random
from . models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from . import tasks


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():

            random_code = random.randint(1000, 9999)
            tasks.otp_send_task(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we sent you a code')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            user_session = request.session['user_registration_info']
            otp_instance = OtpCode.objects.filter(phone_number=user_session['phone_number'])
            if otp_instance.exists():
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.error(request, 'your time is done please make a new one', 'warning')
                return redirect('accounts:user_register')
        except KeyError:
            return redirect('home:home')

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            create_time = code_instance.created + datetime.timedelta(minutes=1)
            tz = timezone("Asia/Tehran")
            now = datetime.datetime.now(tz=tz)
            if cd['code'] == code_instance.code and create_time > now:
                User.objects.create_user(user_session['phone_number'], user_session['email'],
                                         user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'you registered successfully', 'success')
                return redirect('home:home')
            elif create_time < now:
                messages.error(request, 'your expire is done try again', 'danger')
                code_instance.delete()
                return redirect('accounts:user_register')
            else:
                messages.error(request, 'your code is wrong', 'danger')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'your password or phone number is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogOutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')

