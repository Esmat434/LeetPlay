import uuid
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from utils.validators import (
    is_validate_password,is_validate_birth_date
)
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,password,**extrafields):
        if not email:
            raise ValueError("You must enter you email.")
        if not username:
            raise ValueError("You must enter your username.")
        
        email = self.normalize_email(email=email)
        password = is_validate_password(password)
        if type(password) is list:
            raise ValueError(password)
        user = self.model(email = email,username = username,**extrafields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,username,email,password,**extrafields):
        extrafields.setdefault('is_staff',True)
        extrafields.setdefault('is_superuser',True)
        extrafields.setdefault('is_active',True)
        extrafields.setdefault('is_emailverified',True)
        extrafields.setdefault('first_name','admin')
        extrafields.setdefault('last_name','admin')
        extrafields.setdefault('birth_date','2000-02-03')

        if extrafields.get('is_staff') is not True:
            raise ValueError("is_staff of superuser must be True.")
        if extrafields.get('is_superuser') is not True:
            raise ValueError("is_superuser of superuser must be True")
        if extrafields.get('is_emailverified') is not True:
            raise ValueError("is_emailverified of suerpuser must be True")
        return self.create_user(username,email,password,**extrafields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=20,unique=True,db_index=True)
    email = models.EmailField(max_length=100,unique=True)
    first_name = models.CharField(max_length=20,blank=True)
    last_name = models.CharField(max_length=20,blank=True)
    avatar = models.ImageField(upload_to="media/profile/%Y/%m/%d",blank=True)
    birth_date = models.DateField()
    is_emailverified = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(blank=True,null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']

    def __str__(self):
        return self.username


class Password_Token(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def CheckTokenExpiration(self,expiration_minute = 30):
        # count the expiration time
        expiration_time = self.created_at + timedelta(minutes=expiration_minute)

        # in this part check that the time is expired from now
        if timezone.now() > expiration_time:
            return True # token is expired
        else:
            return False # token is not expired