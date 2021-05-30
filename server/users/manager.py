from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, first_name, last_name, password):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email is required'))
        if not first_name:
            raise ValueError('First Name required!')
        if not last_name:
            raise ValueError('Last Name required!')
        if not password:
            raise ValueError(_('Password is required'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name.strip().capitalize(),
                          last_name=last_name.strip().capitalize())
        user.set_password(password)
        user.active = False
        user.writer = False
        user.save()
        return user

    def create_writer(self, email, first_name, last_name, password):
        # creates a writer
        user = self.create_user(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                password=password,
                                )
        user.active = True
        user.writer = True
        user.save()

        return user

    def create_staffuser(self, email, first_name, last_name, password):
        # creates staff user
        user = self.create_user(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                password=password,
                                )
        user.active = True
        user.staff = True
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, password):
        # creates superuser
        user = self.create_user(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                password=password,
                                )
        user.active = True
        user.staff = True
        user.writer = True
        user.admin = True
        user.save()

        return user
