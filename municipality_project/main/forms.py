from django import forms

from municipality_project.auth_app.models import UserProfile, UserDocument
from municipality_project.common.helpers import BootsTrapMixin


class CreateDocumentForm(forms.ModelForm, BootsTrapMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        file = super().save(commit=False)

        file.user = self.user
        if commit:
            file.save()

        return file

    document = forms.FileField(label='Избери файл')

    class Meta:
        model = UserDocument
        fields = ('document', )



class UpdateDocumentForm(forms.ModelForm, BootsTrapMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        file = super().save(commit=False)

        file.user = self.user
        if commit:
            file.save()

        return file

    class Meta:
        model = UserDocument
        fields = ('document', )