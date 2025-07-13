from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContactSerializer, NewsletterSerializer
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@api_view(['POST'])
def contact_form(request):
    serializer = ContactSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the contact form submission
        contact = serializer.save()
        
        # Prepare context for email templates
        context = {
            'name': contact.name,
            'email': contact.email,
            'phone': contact.phone,
            'organization': contact.organization,
            'subject': contact.subject,
            'message': contact.message,
            'inquiry_type': contact.get_inquiry_type_display()
        }
        
        try:
            # Send email to admin
            admin_html = render_to_string('emails/admin_notification.html', context)
            admin_text = strip_tags(admin_html)
            admin_email = EmailMultiAlternatives(
                f"New Contact Form Submission: {contact.subject}",
                admin_text,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL, 'jumashafara0@gmail.com']
            )
            admin_email.attach_alternative(admin_html, "text/html")
            admin_email.send()
            
            # Send confirmation email to user
            user_html = render_to_string('emails/contact_confirmation.html', context)
            user_text = strip_tags(user_html)
            user_email = EmailMultiAlternatives(
                "Thank you for contacting EASI",
                user_text,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email]
            )
            user_email.attach_alternative(user_html, "text/html")
            user_email.send()
            
        except Exception as e:
            print(f"Error sending email: {e}")
            # Still return success even if email fails
            return Response({'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def newsletter_form(request):
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        newsletter = serializer.save()
        
        try:
            # Send confirmation email to newsletter subscriber
            html_content = render_to_string('emails/newsletter_confirmation.html')
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                "Welcome to EASI Newsletter",
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [newsletter.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
        except Exception as e:
            print(f"Error sending newsletter confirmation: {e}")
        
        return Response({'message': 'Newsletter subscription successful'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)