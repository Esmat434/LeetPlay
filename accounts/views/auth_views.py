# django dependencies
from django.conf import settings
from django.shortcuts import HttpResponse,render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.views import View

# app dependencies
from accounts.models import CustomUser,Password_Token
from .mixins import LoginRequiredMixin,LogoutrequiredMixin
from .forms import (
    UserForm,UserUpdateForm,LoginForm,PasswordForgotForm,SetNewPasswordForm
)

# this is registration class view
class CreateUserView(LogoutrequiredMixin,View):

    def get(self,request):
        form = UserForm()
        return render(request,'accounts/signup.html',{'form':form})
    
    def post(self,request):
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.last_login_ip = self.get_client_ip(request)
            user.save()
            return redirect(settings.LOGIN_URL)
        else:
            return render(request,'accounts/signup.html',{'form':form})
    
    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class UpdateUserView(LoginRequiredMixin,View):
    def get(self,request):
        user = get_object_or_404(CustomUser,username = request.user.username)
        form = UserUpdateForm(instance=user)
        return render(request,'accounts/updateAccount.html',{'form':form})
    
    def post(self,request):
        user = get_object_or_404(CustomUser,username = request.user.username)
        form = UserUpdateForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect(settings.PROFILE_URL)
        return render(request,'accounts/updateAccount.html',{'form':form})

# this is login class view
class LoginView(LogoutrequiredMixin,View):
    def get(self,request):
        form = LoginForm()
        return render(request,'accounts/login.html',{'form':form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username = username, password = password)
            if user is not None:
                login(request,user) 
                return redirect(settings.HOME_URL)
            return render(request,'accounts/login.html',{"form":form})
        
        return render(request,'accounts/login.html',{"form":form})

# this is logout class view
class LogoutView(LoginRequiredMixin,View):

    def get(self,request):
        return render(request,'accounts/logout.html')
    
    def post(self,request):
        logout(request)
        return redirect(settings.HOME_URL)

# this is profile class view
class ProfileView(LoginRequiredMixin,View):
    def get_user(self,request):
        try:
            user = CustomUser.objects.get(username = request.user.username)
            return user
        except CustomUser.DoesNotExist:
            return False
        
    def get(self,request):
        user = self.get_user(request)

        if not user:
            return render(request,'accounts/profile.html',{'error':"user does not exists."})
    
        return render(request,'accounts/profile.html',{'user':user})
    
# this is password forgot class view
class PasswrdForgotView(LogoutrequiredMixin,View):
    def get(self,request):
        form = PasswordForgotForm()
        return render(request,'accounts/password_forgot.html',{'form':form})

    def post(self,request):
        email = request.POST.get('email')
        form = PasswordForgotForm(request.POST)
        user = self.get_user_by_email(email)
        if form.is_valid():
            token,_ = Password_Token.objects.get_or_create(user = user)
            return render(request,'accounts/message.html')
        return render(request,'accounts/password_forgot.html',{'error':"your email is invalid."})

    def get_user_by_email(self,email):
        try:
            user = CustomUser.objects.get(email = email)
            return user
        except CustomUser.DoesNotExist:
            return None

# this is set new password class view that can set new password if you forgot your password
class SetNewPasswordView(LogoutrequiredMixin,View):
    
    def get_token(self,key):
        if isinstance(key,str) or isinstance(key,int):
            return False
        try:
            token = Password_Token.objects.get(token = key)
        except Password_Token.DoesNotExist:
            return False
        
        if token.CheckTokenExpiration():
            token.delete()
            return False
        return token
    
    def get(self,request,token):
        token = self.get_token(token)
        form = SetNewPasswordForm()
        if not token:
            return render(request,'accounts/error.html',{'error':'Your token is expired Please create another token.','status_code':400})
        return render(request,'accounts/set_password.html',{'form':form})
    
    def post(self,request,token):
        token = self.get_token(token)
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1','')
            token.user.set_password(password)
            token.user.save()
            token.delete()
            return redirect(settings.LOGIN_URL)
        return render(request,'accounts/set_password.html',{'form':form})

def index(request):
    return HttpResponse()