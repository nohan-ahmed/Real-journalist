from django.contrib.auth.models import BaseUserManager

class Manager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email most be set.')
        
        email = self.normalize_email(email=email)
        user = self.model(email=email, username=username, **extra_fields) # Create an user instance without saving into DB.
        user.set_password(password) # hash raw password and set
        user.save(using=self.db)
        return user
        
    def createuser_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_supseruser', True)
        return self.create_user(email, username, password, **extra_fields)