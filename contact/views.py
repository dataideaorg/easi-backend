from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContactSerializer, NewsletterSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@api_view(['POST'])
def contact_form(request):
    serializer = ContactSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the contact form submission
        contact = serializer.save()
        
        # Send email notification to admin
        admin_subject = f"New Contact Form Submission: {contact.subject}"
        admin_message = f"""
        Name: {contact.name}
        Email: {contact.email}
        Phone: {contact.phone}
        Organization: {contact.organization}
        Inquiry Type: {contact.get_inquiry_type_display()}
        
        Message:
        {contact.message}
        """
        
        # Send confirmation email to user
        user_subject = "Thank you for contacting EASI"
        user_message = f"""
        Dear {contact.name},

        Thank you for contacting the East African Statistics Institute (EASI). We have received your inquiry regarding "{contact.subject}".

        We will review your message and get back to you as soon as possible. Here's a copy of your message for your records:

        Subject: {contact.subject}
        Inquiry Type: {contact.get_inquiry_type_display()}
        Message:
        {contact.message}

        If you have any additional questions, please don't hesitate to reach out.

        Best regards,
        EASI Team
        """
        
        try:
            # Send email to admin
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL, 'jumashafara0@gmail.com'],
                fail_silently=False,
            )
            
            # Send confirmation email to user
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email],  # Send to the user's email
                fail_silently=False,
            )
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
        
        # Send confirmation email to newsletter subscriber
        subject = "Welcome to EASI Newsletter"
        message = f"""
        Dear Subscriber,

        Thank you for subscribing to the EASI newsletter! We're excited to have you join our community.

        You will now receive updates about:
        - Latest statistical research and methodologies
        - Upcoming training programs and workshops
        - News and events from EASI
        - Resources and publications

        If you wish to unsubscribe at any time, please contact us.

        Best regards,
        EASI Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [newsletter.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending newsletter confirmation: {e}")
        
        return Response({'message': 'Newsletter subscription successful'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)