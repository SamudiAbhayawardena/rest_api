from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _ 

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            #validate email
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Invalid Email"))
    
    # normal user creation
    def create_user(self, email, password, **extra):
        if email:
            email = self.normalize_email(email=email)
            self.email_validator(email=email)
        else:
            raise ValueError(_('Email Required'))
        user=self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # create super user
    def create_superuser(self, email, password, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("is_verified", True)

        if extra.get("is_staff") is not True:
            raise ValueError(_("Not Staff"))

        if extra.get("is_superuser") is not True:
            raise ValueError(_("Not Superuser"))
        
        user = self.create_user(email, password, **extra)
        user.save(using=self._db)
        return user