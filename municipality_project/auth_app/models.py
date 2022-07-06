from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save

from municipality_project.auth_app.managers import ProjectUserManager
from municipality_project.auth_app.validators import only_letters_validator


class ProjectUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LENGTH = 30
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=(
            MinLengthValidator(2),
            only_letters_validator,
        )
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = ProjectUserManager()


class UserProfile(models.Model):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 20

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH
    )

    email = models.EmailField()

    # email_confirmed = models.BooleanField(
    #     default=False
    # )

    user = models.OneToOneField(
        ProjectUser,
        on_delete=models.CASCADE,
        primary_key=True,

    )

class UserDocument(models.Model):
    document = models.FileField(
        upload_to='user_files/'
    )

    user = models.OneToOneField(
        ProjectUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.document}'

from django.dispatch import receiver


@receiver(post_save, sender=ProjectUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(
            user=instance,
        )
        profile.save()




# @receiver(post_save, sender=ProjectUser)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()