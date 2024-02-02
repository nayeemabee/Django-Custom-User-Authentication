from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Must have an Eamil")

        # normalizing email 
        user = self.model(email= self.normalize_email(email), **extra_fields)

        #  setting password uaing ste_password method
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        # if not true raise eror 
        if extra_fields.get('is_admin') is not True:
            raise ValueError("SuperUser must have is_admin=True")
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):

    # custom field that we want to define 
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50)
    dob = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=12, blank=True, null=True)
    address = models.TextField()
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # MAking Django to Use Our defined User Manager for this custom user.
    objects = UserManager()

    # making email to use for login instead of username, we can give anyother thing like mobile_number, but it should be unique in DB.
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_lable):
        return True
    
    # defining is_staff property as is_admin (boolean)  - by default False (Line no. 43)
    @property
    def is_staff(self):
        return self.is_admin