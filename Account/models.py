from django.db import models
# extend django user model AND CREATE YOUR OWN user model.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

#Receive the signal that a user has been created and create a token as well
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Manager class -> can create a user or super user
# all of this class is BoilerPlate
class MyAccountUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        # if not username:
        #     raise ValueError('Users must have a username')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user
        
    # Override the create_superuser function
    # Creates a super user, -> usually used within the command line
    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# This is the ACTUAL class MODEL/TABLE/SCHEMA for ALL Users


class Account(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="email")
    # username = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(max_length=255, default="local", null=False)
    social_id = models.CharField(max_length=255, default=None, null=True)
    fullname = models.CharField(max_length=255, default=None, null=True)
    firstname = models.CharField(max_length=255, default=None, null=True)
    lastname = models.CharField(max_length=255, default=None, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # KEYWORD THAT WE NEED TO SPECIFY to user 'email' as username
    USERNAME_FIELD = 'email'
    # any other field that we want to require in the User model
    # REQUIRED_FIELDS = ['username']

    # Creates a new MyAccountUserManager Model for our objects
    # SO, when we call this Account class,
    # we have access to all of the User details(columns) we define in this Model/table
    objects = MyAccountUserManager()

    def __str__(self):
        return self.email

    def set_social_id(self, social_id):
        self.social_id = social_id


#THIS WILL GET CALLED AFTER WE CREATE A NEW USER.
#Receive the signal that a user has been created using the custom AUTH_USER_MODEL and create a token as well
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
