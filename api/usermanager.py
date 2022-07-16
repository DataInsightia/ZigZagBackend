from django.db import models
from django.contrib.auth.models import BaseUserManager

 
class MyUserManager(BaseUserManager):
   def create_user(self, login_id,mobile=None,password=None):
       """
       Creates and saves a User with the given login ID,and password.
       """
       if not login_id:
           raise ValueError('Users must have an login ID')
 
       user = self.model(login_id = login_id,mobile = mobile)
       user.set_password(password)
       user.save(using=self._db)
       return user
 
   def create_superuser(self, login_id,mobile=None,password=None):
       """
       Creates and saves a superuser with the given login ID, password.
       """
       user = self.create_user(login_id,mobile = mobile,password=password)
       user.is_admin = True
       user.save(using=self._db)
       return user