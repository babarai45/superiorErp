#!/usr/bin/env python
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superiorErp.settings')
django.setup()

from accounts.models import User, StudentProfile

# Your credentials from admission
email = "student.su25-bsse-s24-003@superior.edu.pk"
roll_number = "su25-bsse-s24-003"

# Delete if exists
User.objects.filter(email=email).delete()
StudentProfile.objects.filter(roll_number=roll_number).delete()

# Create user
user = User.objects.create_user(
    email=email,
    password=roll_number,
    username=roll_number,
    first_name="Muhammad",
    last_name="Babar",
    role="student",
    is_active=True,
    is_verified=True,
)

# Create student profile with unique personal email
profile = StudentProfile.objects.create(
    user=user,
    roll_number=roll_number,
    father_name="Ahmed",
    cnic="3730123456780",  # Unique CNIC
    date_of_birth=date(2004, 3, 15),
    gender="M",
    personal_email="muhammadbabar@example.com",  # Unique email
    university_email=email,
    whatsapp_number="03009876543",
    intake="spring",
    program="BSSE",
    is_approved=True,
)

print(f"✓ User created: {email}")
print(f"✓ Password: {roll_number}")
print(f"✓ Ready to login!")

