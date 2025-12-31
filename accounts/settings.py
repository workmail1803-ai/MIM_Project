# settings.py

# For Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not regular password

# For development - use environment variables
import os
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@wondrneub.edu.bd'
SERVER_EMAIL = 'noreply@wondrneub.edu.bd'
# settings.py

# Use console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Optional: File-based email backend (saves emails to files)
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/app-emails'  # Create this directory

# Basic email settings
DEFAULT_FROM_EMAIL = 'noreply@wondrneub.edu.bd'
SERVER_EMAIL = 'noreply@wondrneub.edu.bd'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Shows emails in console
DEFAULT_FROM_EMAIL = 'noreply@wondrneub.edu.bd'
SERVER_EMAIL = 'noreply@wondrneub.edu.bd'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-emails' 