"""
Management script to create sample users with proper passwords
Run: python create_sample_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodshare_project.settings')
django.setup()

from django.contrib.auth.models import User
from bloodshare.models import Profile, DonationRequest
from datetime import date, timedelta

# Sample user data
sample_users = [
    {
        'username': 'alice.johnson@example.com',
        'email': 'alice.johnson@example.com',
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'phone': '+1-555-0101',
        'blood_group': 'O+',
        'city': 'New York',
        'is_available': True,
    },
    {
        'username': 'bob.smith@example.com',
        'email': 'bob.smith@example.com',
        'first_name': 'Bob',
        'last_name': 'Smith',
        'phone': '+1-555-0102',
        'blood_group': 'A+',
        'city': 'Los Angeles',
        'is_available': True,
    },
    {
        'username': 'charlie.brown@example.com',
        'email': 'charlie.brown@example.com',
        'first_name': 'Charlie',
        'last_name': 'Brown',
        'phone': '+1-555-0103',
        'blood_group': 'B+',
        'city': 'Chicago',
        'is_available': False,
    },
    {
        'username': 'diana.prince@example.com',
        'email': 'diana.prince@example.com',
        'first_name': 'Diana',
        'last_name': 'Prince',
        'phone': '+1-555-0104',
        'blood_group': 'AB+',
        'city': 'Houston',
        'is_available': True,
    },
    {
        'username': 'edward.norton@example.com',
        'email': 'edward.norton@example.com',
        'first_name': 'Edward',
        'last_name': 'Norton',
        'phone': '+1-555-0105',
        'blood_group': 'O-',
        'city': 'Phoenix',
        'is_available': True,
    },
]

# Delete existing sample users if they exist
for user_data in sample_users:
    User.objects.filter(email=user_data['email']).delete()

# Create users and profiles
for user_data in sample_users:
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password='SamplePass123!',  # Set a real password
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )
    Profile.objects.create(
        user=user,
        phone=user_data['phone'],
        blood_group=user_data['blood_group'],
        city=user_data['city'],
        is_available=user_data['is_available'],
        last_donation_date=date.today() - timedelta(days=90) if user_data['is_available'] else None
    )
    print(f"Created user: {user.get_full_name()} ({user_data['blood_group']}) - {user_data['city']}")

# Create some donation requests
if User.objects.filter(email='alice.johnson@example.com').exists():
    user1 = User.objects.get(email='alice.johnson@example.com')
    DonationRequest.objects.create(
        requester=user1,
        name='John Doe',
        blood_group_needed='O+',
        city='New York',
        details='Urgent need for surgery',
        status='pending'
    )

if User.objects.filter(email='bob.smith@example.com').exists():
    user2 = User.objects.get(email='bob.smith@example.com')
    DonationRequest.objects.create(
        requester=user2,
        name='Jane Smith',
        blood_group_needed='A+',
        city='Los Angeles',
        details='Emergency transfusion needed',
        status='pending'
    )

print("\n" + "="*50)
print("Sample data created successfully!")
print("="*50)
print("\nYou can login with any of these accounts:")
print("Password for all: SamplePass123!")
print("\nUsers:")
for user_data in sample_users:
    print(f"  - {user_data['email']} ({user_data['blood_group']}, {user_data['city']})")

