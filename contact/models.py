from django.db import models

class Contact(models.Model):
    INQUIRY_CHOICES = [
        ('general', 'General Inquiry'),
        ('training', 'Training Programs'),
        ('consultancy', 'Consultancy Services'),
        ('partnership', 'Partnership Opportunities'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    organization = models.CharField(max_length=100, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_CHOICES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}" 
    
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
