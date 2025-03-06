from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ContactSerializer, NewsletterSerializer
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
def contact_form(request):
    serializer = ContactSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the contact form submission
        contact = serializer.save()
        
        # Send email notification
        subject = f"New Contact Form Submission: {contact.subject}"
        message = f"""
        Name: {contact.name}
        Email: {contact.email}
        Phone: {contact.phone}
        Organization: {contact.organization}
        Inquiry Type: {contact.get_inquiry_type_display()}
        
        Message:
        {contact.message}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Add your contact email in settings
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
        
        return Response({'message': 'Contact form submitted successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
def newsletter_form(request):
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Newsletter form submitted successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)