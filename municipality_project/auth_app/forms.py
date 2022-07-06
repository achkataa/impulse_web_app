from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from municipality_project.auth_app.models import UserProfile
from municipality_project.common.helpers import BootsTrapMixin
from django.utils.translation import gettext_lazy as _
# class RegisterUserForm(UserCreationForm, BootsTrapMixin):
#     first_name = forms.CharField(
#         max_length=UserProfile.FIRST_NAME_MAX_LENGTH,
#         label='Собствено Име'
#     )
#     last_name = forms.CharField(
#         max_length=UserProfile.LAST_NAME_MAX_LENGTH,
#         label='Фамилия'
#     )
#     email = forms.EmailField(
#         label='Имейл'
#     )
#
#     username = forms.CharField(label='Потребителско Име')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._init_bootstrap_form_controls()
#
#     def save(self, commit=True):
#         user = super().save(commit=commit)
#         user_profile = UserProfile(
#             first_name=self.cleaned_data['first_name'],
#             last_name=self.cleaned_data['last_name'],
#             email=self.cleaned_data['email'],
#             user=user,
#         )
#
#         if commit:
#             user_profile.save()
#         return user
#
#
#     class Meta:
#         model = get_user_model()
#         fields = ('username', )


class RegisterUserForm(UserCreationForm, BootsTrapMixin):
    first_name = forms.CharField(
        max_length=UserProfile.FIRST_NAME_MAX_LENGTH,
        label='Собствено Име'
    )
    last_name = forms.CharField(
        max_length=UserProfile.LAST_NAME_MAX_LENGTH,
        label='Фамилия'
    )
    email = forms.EmailField(
        label='Имейл'
    )

    username = forms.CharField(label='Потребителско Име')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    # def save(self, commit=True):
    #     user = super().save(commit=commit)
    #     user_profile = UserProfile(
    #         first_name=self.cleaned_data['first_name'],
    #         last_name=self.cleaned_data['last_name'],
    #         email=self.cleaned_data['email'],
    #         user=user,
    #     )
    #
    #     if commit == True:
    #         user_profile.save()
    #     return user


    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')



class LoginUserForm(BootsTrapMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    username = forms.CharField(label='Име на потребителя')
