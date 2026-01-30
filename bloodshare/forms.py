from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, DonationRequest, BLOOD_GROUP_CHOICES


class SignUpForm(UserCreationForm):
    """User registration form with profile fields"""
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Full Name',
            'aria-label': 'Full Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email',
            'aria-label': 'Email'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'aria-label': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm Password',
            'aria-label': 'Confirm Password'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone (optional)',
            'aria-label': 'Phone Number'
        })
    )
    blood_group = forms.ChoiceField(
        choices=[('', 'Select Blood Group')] + BLOOD_GROUP_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'aria-label': 'Blood Group'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'City (optional)',
            'aria-label': 'City'
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-input',
            'accept': 'image/*',
            'aria-label': 'Avatar Upload'
        })
    )
    agree_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
            'aria-label': 'I agree to the terms and conditions'
        })
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2', 'phone', 'blood_group', 'city', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name'].split()[0] if self.cleaned_data['full_name'] else ''
        if len(self.cleaned_data['full_name'].split()) > 1:
            user.last_name = ' '.join(self.cleaned_data['full_name'].split()[1:])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                blood_group=self.cleaned_data.get('blood_group', ''),
                city=self.cleaned_data.get('city', ''),
            )
            if self.cleaned_data.get('avatar'):
                profile.avatar = self.cleaned_data['avatar']
                profile.save()
        return user


class LoginForm(forms.Form):
    """User login form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email',
            'aria-label': 'Email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'aria-label': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
            'aria-label': 'Remember me'
        })
    )


class ProfileForm(forms.ModelForm):
    """Profile edit form"""
    full_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'aria-label': 'Full Name'
        })
    )

    class Meta:
        model = Profile
        fields = ['phone', 'blood_group', 'city', 'avatar', 'last_donation_date']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input', 'aria-label': 'Phone'}),
            'blood_group': forms.Select(attrs={'class': 'form-input', 'aria-label': 'Blood Group'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'aria-label': 'City'}),
            'avatar': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*', 'aria-label': 'Avatar'}),
            'last_donation_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'aria-label': 'Last Donation Date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['full_name'].initial = self.user.get_full_name()

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            if self.cleaned_data.get('full_name'):
                name_parts = self.cleaned_data['full_name'].split()
                self.user.first_name = name_parts[0] if name_parts else ''
                self.user.last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                self.user.save()
        return profile


class DonationRequestForm(forms.ModelForm):
    """Form to create donation requests"""
    class Meta:
        model = DonationRequest
        fields = ['name', 'blood_group_needed', 'city', 'details']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Name of person needing blood',
                'aria-label': 'Name'
            }),
            'blood_group_needed': forms.Select(attrs={
                'class': 'form-input',
                'aria-label': 'Blood Group Needed'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City',
                'aria-label': 'City'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional details (optional)',
                'rows': 4,
                'aria-label': 'Details'
            }),
        }

