from django.db import models
from datetime import datetime

class Inquiry(models.Model):
  listing_id = models.IntegerField()
  listing = models.CharField(max_length=200)
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  phone = models.CharField(max_length=100)
  message = models.TextField(blank=True)
  inquiry_date = models.DateTimeField(default=datetime.now, blank=True)
  user_id = models.IntegerField(blank=True)
  class Meta:
    verbose_name_plural = "Inquiries"
  def __str__(self):
    return self.name
