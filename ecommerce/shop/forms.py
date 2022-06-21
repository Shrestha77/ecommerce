from django import forms
from shop import models


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('email', 'first_name', 'middle_name',
                  'last_name', 'password1', 'password2', 'user_name', 'contact')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = ['name', 'email', 'message', 'phone']
            

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['user_name', 'first_name',
                  'last_name',  'profile', 'contact']
