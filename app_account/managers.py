from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, name, password=None):
        if not phone:
            raise ValueError('Users must have an phone')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            phone=phone,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, name, password=None):

        user = self.create_user(
            phone=phone,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user