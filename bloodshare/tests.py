from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Profile, DonationRequest


class ProfileModelTest(TestCase):
    """Test Profile model behavior"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_profile_creation(self):
        """Test that a profile is created when user is created"""
        profile = Profile.objects.create(
            user=self.user,
            phone='+1234567890',
            blood_group='O+',
            city='Test City',
            is_available=True
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, '+1234567890')
        self.assertEqual(profile.blood_group, 'O+')
        self.assertEqual(profile.city, 'Test City')
        self.assertTrue(profile.is_available)
    
    def test_profile_str_representation(self):
        """Test Profile string representation"""
        profile = Profile.objects.create(
            user=self.user,
            blood_group='A+'
        )
        expected = f"{self.user.get_full_name()} - A+"
        self.assertEqual(str(profile), expected)
    
    def test_profile_one_to_one_relationship(self):
        """Test that Profile has one-to-one relationship with User"""
        profile = Profile.objects.create(user=self.user)
        # Should not be able to create another profile for same user
        with self.assertRaises(Exception):
            Profile.objects.create(user=self.user)


class DonationRequestModelTest(TestCase):
    """Test DonationRequest model behavior"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_donation_request_creation(self):
        """Test creating a donation request"""
        request = DonationRequest.objects.create(
            requester=self.user,
            name='John Doe',
            blood_group_needed='B+',
            city='New York',
            details='Urgent need for blood',
            status='pending'
        )
        self.assertEqual(request.requester, self.user)
        self.assertEqual(request.name, 'John Doe')
        self.assertEqual(request.blood_group_needed, 'B+')
        self.assertEqual(request.city, 'New York')
        self.assertEqual(request.status, 'pending')
    
    def test_donation_request_str_representation(self):
        """Test DonationRequest string representation"""
        request = DonationRequest.objects.create(
            requester=self.user,
            name='Jane Smith',
            blood_group_needed='AB-',
            city='Los Angeles'
        )
        expected = "Jane Smith - AB- - Los Angeles"
        self.assertEqual(str(request), expected)
    
    def test_donation_request_default_status(self):
        """Test that donation request defaults to pending status"""
        request = DonationRequest.objects.create(
            requester=self.user,
            name='Test Name',
            blood_group_needed='O+',
            city='Test City'
        )
        self.assertEqual(request.status, 'pending')
    
    def test_donation_request_ordering(self):
        """Test that donation requests are ordered by created_at descending"""
        request1 = DonationRequest.objects.create(
            requester=self.user,
            name='First Request',
            blood_group_needed='A+',
            city='City1'
        )
        request2 = DonationRequest.objects.create(
            requester=self.user,
            name='Second Request',
            blood_group_needed='B+',
            city='City2'
        )
        requests = list(DonationRequest.objects.all())
        self.assertEqual(requests[0], request2)  # Most recent first
        self.assertEqual(requests[1], request1)


class SignUpFlowTest(TestCase):
    """Test user signup flow"""
    
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
    
    def test_signup_page_loads(self):
        """Test that signup page loads successfully"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Your Account')
    
    def test_signup_with_valid_data(self):
        """Test successful user signup with valid data"""
        data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'phone': '+1234567890',
            'blood_group': 'O+',
            'city': 'New York',
            'agree_to_terms': True
        }
        response = self.client.post(self.signup_url, data)
        
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        
        # User should be created
        user = User.objects.get(email='john@example.com')
        self.assertEqual(user.username, 'john@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        
        # Profile should be created
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.phone, '+1234567890')
        self.assertEqual(profile.blood_group, 'O+')
        self.assertEqual(profile.city, 'New York')
    
    def test_signup_with_duplicate_email(self):
        """Test that signup fails with duplicate email"""
        User.objects.create_user(
            username='existing@example.com',
            email='existing@example.com',
            password='testpass123'
        )
        
        data = {
            'full_name': 'New User',
            'email': 'existing@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'agree_to_terms': True
        }
        response = self.client.post(self.signup_url, data)
        
        # Should not redirect (form errors)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')
        
        # Should only have one user with this email
        self.assertEqual(User.objects.filter(email='existing@example.com').count(), 1)
    
    def test_signup_with_mismatched_passwords(self):
        """Test that signup fails with mismatched passwords"""
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'agree_to_terms': True
        }
        response = self.client.post(self.signup_url, data)
        
        # Should not redirect (form errors)
        self.assertEqual(response.status_code, 200)
        # Check that form has errors on password2 field
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertTrue('password2' in form.errors)
    
    def test_signup_without_terms_agreement(self):
        """Test that signup fails without terms agreement"""
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'agree_to_terms': False
        }
        response = self.client.post(self.signup_url, data)
        
        # Should not redirect (form errors)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'agree_to_terms', ['This field is required.'])
    
    def test_signup_with_optional_fields(self):
        """Test signup with only required fields"""
        data = {
            'full_name': 'Minimal User',
            'email': 'minimal@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'agree_to_terms': True
        }
        response = self.client.post(self.signup_url, data)
        
        # Should succeed
        self.assertEqual(response.status_code, 302)
        
        user = User.objects.get(email='minimal@example.com')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.phone, '')
        self.assertEqual(profile.blood_group, '')
        self.assertEqual(profile.city, '')
    
    def test_signup_user_is_logged_in(self):
        """Test that user is automatically logged in after signup"""
        data = {
            'full_name': 'Auto Login User',
            'email': 'autologin@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'agree_to_terms': True
        }
        response = self.client.post(self.signup_url, data)
        
        # User should be logged in
        user = User.objects.get(email='autologin@example.com')
        self.assertTrue(self.client.session.get('_auth_user_id') == str(user.id))


class LoginFlowTest(TestCase):
    """Test user login flow"""
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome Back')
    
    def test_login_with_valid_credentials(self):
        """Test successful login with valid credentials"""
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_login_with_invalid_credentials(self):
        """Test login fails with invalid credentials"""
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        
        # Should not redirect
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password')
    
    def test_login_redirects_authenticated_users(self):
        """Test that authenticated users are redirected from login page"""
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))


class DashboardTest(TestCase):
    """Test dashboard functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            blood_group='O+',
            city='Test City'
        )
    
    def test_dashboard_requires_authentication(self):
        """Test that dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_loads_for_authenticated_user(self):
        """Test that dashboard loads for authenticated user"""
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back')
    
    def test_dashboard_shows_user_profile(self):
        """Test that dashboard displays user profile information"""
        self.client.login(username='testuser@example.com', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'O+')
        self.assertContains(response, 'Test City')
