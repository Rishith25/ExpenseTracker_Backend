from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
        # user.set_password(password)
        # user.save(using=self._db)
        # return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.set_password(self.password)
    #     super().save(*args, **kwargs)
        
    def __str__(self):
        return self.email

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_no = models.DecimalField(max_digits=10, decimal_places=0, primary_key = True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False, null=True)

class FinancialTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_no = models.ForeignKey(Account, on_delete=models.CASCADE) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    category = models.CharField(max_length=255)
    TRANSACTION_TYPES = [('income', 'Income'), ('expense', 'Expense')]
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    mode_of_payment = models.CharField(max_length=100)
    description = models.TextField()
    attachment = models.URLField(blank=True, null=True)
