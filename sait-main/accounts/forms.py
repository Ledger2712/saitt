from django import forms
from django.contrib.auth.models import User

class SimpleRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')
        labels = {
            'first_name': 'Имя',
            'email': 'Адрес электронной почты',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким e-mail уже существует")
        return email

    def save(self, commit=True):
        # создаём пользователя, используем e-mail как username
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
