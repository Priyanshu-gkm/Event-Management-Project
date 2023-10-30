from django.contrib.auth.models import BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, username,email=None,role="OTHERS", password=None):
        if not username:
            return ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email).lower(),
            username=username,
            password = password,
        )
        user.role=role
        user.is_active = True
        
        if role=="ORGANIZER":
            user.is_staff=True
        
        if role=="ADMIN":
            user.is_staff=True
            user.is_admin=True

        user.set_password(password)
        user.save(using=self._db)
        
        return user


    def create_superuser(self, username,email=None,role="OTHERS", password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            username = username,
            role=role
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin=True
        user.save(using=self._db)
        return user
