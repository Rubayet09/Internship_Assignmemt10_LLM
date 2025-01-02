from django.db import models

class ScrapedProperty(models.Model):
    """Model representing the original scraped properties"""
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    rating = models.FloatField(null=True)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    room_type = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    image_path = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'properties'  # Match the existing table name
        managed = False # Remove managed = False so Django can manage other tables

class PropertySummary(models.Model):
    """Model for storing AI-generated property summaries"""
    property = models.OneToOneField(ScrapedProperty, on_delete=models.CASCADE, primary_key=True)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Remove managed = False to let Django create this table

class PropertyReview(models.Model):
    """Model for storing AI-generated property reviews and ratings"""
    property = models.OneToOneField(ScrapedProperty, on_delete=models.CASCADE, primary_key=True)
    rating = models.FloatField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Remove managed = False to let Django create this table