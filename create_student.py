import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'os_djangopro.settings')
django.setup()

from django.contrib.auth.models import User

# Create student2
try:
    user = User.objects.create_user(
        username='student2',
        password='student@123',
        email='student2@neub.edu.bd'
    )
    print("✓ Student 2 created successfully!")
    print("\nLogin Credentials:")
    print("==================")
    print("Username: student2")
    print("Password: student@123")
    print("Email: student2@neub.edu.bd")
except Exception as e:
    print(f"Error: {e}")
