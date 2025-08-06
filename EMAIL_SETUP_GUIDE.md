# Email Configuration Guide for Bhanubhakta Campus

## To enable email functionality, update the following in settings.py:

EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Your Gmail app password
CONTACT_EMAIL = 'bhanubhaktacampus240@gmail.com'  # Where contact forms will be sent

## Steps to get Gmail App Password:

1. Go to your Google Account settings
2. Security → 2-Step Verification (enable if not already)
3. App passwords → Select "Mail" → Generate
4. Use the generated 16-character password in EMAIL_HOST_PASSWORD

## Test the contact form:

1. Fill out the contact form on your website
2. Check your email at bhanubhaktacampus240@gmail.com
3. Check the Django admin panel for saved contact messages

## Features now working:

✅ Contact form saves to database
✅ Email notifications sent to campus email
✅ Admin panel for managing contact messages
✅ Form validation and error handling
✅ Success/error messages to users
✅ Works on both home page and contact page

## Admin Panel Access:

Visit: http://127.0.0.1:8000/admin/
Look for "Contact Messages" section to view all submissions.
