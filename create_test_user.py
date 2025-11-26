#!/usr/bin/env python
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superiorErp.settings')
django.setup()

from accounts.models import User, StudentProfile

# Test user credentials
email = "student.su25-bsse-s24-002@superior.edu.pk"
roll_number = "su25-bsse-s24-002"

# Delete if exists
User.objects.filter(email=email).delete()
StudentProfile.objects.filter(roll_number=roll_number).delete()

# Create new user
user = User.objects.create_user(
    email=email,
    password=roll_number,
    username=roll_number,
    first_name="Babar",
    role="student",
    is_active=True,
    is_verified=True,
)

# Create student profile
profile = StudentProfile.objects.create(
    user=user,
    roll_number=roll_number,
    father_name="Ahmed",
    cnic="3730123456789",
    date_of_birth=date(2004, 3, 15),
    gender="M",
    personal_email="babar@example.com",
    university_email=email,
    whatsapp_number="03009876543",
    intake="fall",
    program="BSSE",
    is_approved=True,
)

print(f"✓ User created: {email}")
print(f"✓ Password: {roll_number}")
print(f"✓ StudentProfile created")
print(f"✓ Ready to login!")

