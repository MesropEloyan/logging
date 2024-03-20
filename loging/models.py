from django.contrib.auth.models import User
from django.db import models

class Document(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)  # Character field
    quantity = models.IntegerField()  # Integer field
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field
    url = models.URLField()  # URL field
    email = models.EmailField()  # Email field
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    is_active = models.BooleanField(default=False)  # Boolean field
    ip_address = models.GenericIPAddressField()  # IP address field


    def __str__(self):
        return self.name

class DocumentHistory(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    field_name = models.CharField(max_length=100, blank=True)
    before_edit = models.CharField(max_length=100, blank=True)
    after_edit =  models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.action} - {self.user} - {self.created_at} "