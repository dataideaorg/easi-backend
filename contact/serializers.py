from rest_framework import serializers
from .models import Contact, Newsletter

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message', 'organization', 'inquiry_type'] 

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email']
