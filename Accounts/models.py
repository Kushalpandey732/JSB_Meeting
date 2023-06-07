from django.db import models
from datetime import date, timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.

# Creat Department
class Department(models.Model):
    Dept_Name = models.CharField(max_length=150)

    def __str__(self):
        return self.Dept_Name
    
    class Meta:
        verbose_name_plural = 'Department'

# Create Sub Department
class Sub_Department(models.Model):
    Sub_Dept_Name = models.CharField(max_length=150)
    Department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Sub_Dept_Name

    class Meta:
        verbose_name_plural = 'Sub Department'


# Subsidiary Table
class Subsidiary(models.Model):
    Subs_Name = models.CharField(max_length=150)

    def __str__(self):
        return self.Subs_Name

    class Meta:
        verbose_name_plural = 'Subsidiary'

# Priority Table
class Priority(models.Model):
    Priority_Name = models.CharField(max_length=50)

    def __str__(self):
        return self.Priority_Name

    class Meta:
        verbose_name_plural = 'Priority'
    
# Status Table
class Status(models.Model):
    Status_Desc = models.CharField(max_length=50)

    def __str__(self):
        return self.Status_Desc

    class Meta:
        verbose_name_plural = 'Status'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, email, password, subsidiary=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username,email=email, subsidiary=subsidiary, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username=None, subsidiary=None):
        """
        Create and save a SuperUser with the given email and password.
        """

        u = self.create_user(username,email,
                        password=password,
                        subsidiary=subsidiary
                    )
        u.is_admin = True
        u.save(using=self._db)
        return u
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError(_('Superuser must have is_superuser=True.'))
        # return self.create_user(email, password, department, subsidiary, **extra_fields)

# Create your models here.
class JSBUsers(AbstractBaseUser):
    username = models.CharField(
        max_length=255, null=True,
    )
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=date.today)
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.CASCADE, default=None, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    objects = CustomUserManager()

    def __str__(self):
        return self.email