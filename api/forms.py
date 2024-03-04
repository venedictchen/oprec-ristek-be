from money_app.models import ProfileUser
from django import forms
class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['user', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country', 'avatar']