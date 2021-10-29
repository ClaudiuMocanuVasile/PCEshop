from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import *



class RegistrationForm(UserCreationForm):

    """This class inherits from the UserCreationForm class

       Additions: 
        
       added first_name, last_name fields needed for Customer class

       added address, city, county, zipcode fields needed for 
       ShippingAddress class

       added clean_email function
    """


    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )

    
    address = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    
    city = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    
    county = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    
    zipcode = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'border w-full h-5 px-3 py-5 mt-2 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )


    def clean_email(self):

        """This function overrides the default clean_email function
           and prevents account creation with duplicate email during 
           user registration
        """


        email = self.cleaned_data['email']

        if not Customer.objects.all().filter(email = email).values('email'):
            return email
        else:
            raise forms.ValidationError('This email address is already in use.')


    class Meta(UserCreationForm.Meta):

        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)



class UploadForm(forms.ModelForm):

    """This form is used for uploading a profile user photo
       in the user profile page
    """


    image = forms.FileField(
        widget = forms.ClearableFileInput(
            attrs = {
                'class': 'hidden profile_pic_upload', 
                'accept':'image/*', 
                'required': 'false'
            }
        )
    )


    class Meta:

        model = Customer
        fields = ['image']



class DeleteUser(forms.ModelForm):

    """This class inherits from ModelForm and is used for
       user deletion in the user profile page
    """


    username = forms.IntegerField(
        widget = forms.TextInput(
            attrs = {
                'class':'hidden'
            }
        )
    )


    class Meta:

        model = User
        fields = ['username']



class ResetPasswordForm(PasswordResetForm):

    """This class inherits from PasswordResetForm and serves as a
       custom form that can be used in a custom template for the
       PasswordResetView
    """


    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)


    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class': 'border w-full mr-3 h-5 px-3 py-5 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )



class ResetPasswordConfirmForm(SetPasswordForm):

    """This class inherits from SetPasswordForm and serves as a
       custom form that can be used in a custom template for the 
       PasswordResetConfirmView
    """


    def __init__(self, *args, **kwargs):
        super(ResetPasswordConfirmForm, self).__init__(*args, **kwargs)


    new_password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'border w-full mr-3 h-5 px-3 py-5 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )
    
    new_password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'class': 'border w-full mr-3 h-5 px-3 py-5 hover:outline-none focus:outline-none focus:ring-1 focus:ring-blue-800 rounded-md shadow-md'
            }
        )
    )

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]