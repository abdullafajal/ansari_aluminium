from django.db import models

class ContactEnquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        CONVERTED = "converted", "Converted"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    
    # Status tracking
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    notes = models.TextField(blank=True)
    
    # Link to converted customer
    customer = models.ForeignKey(
        "customers.Customer", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="enquiries"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False) # Keep for backward compatibility

    class Meta:
        verbose_name_plural = "Contact Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
