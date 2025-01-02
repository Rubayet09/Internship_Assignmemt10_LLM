from ..models import ScrapedProperty, PropertySummary, PropertyReview
from .gemini_service import GeminiService

class PropertyService:
    def __init__(self):
        self.gemini_service = GeminiService()

    def process_all_properties(self):
        """Process all properties and generate AI content"""
        properties = ScrapedProperty.objects.all()
        total = properties.count()
        
        for index, property_data in enumerate(properties, 1):
            print(f"Processing property {index}/{total}: {property_data.title}")
            
            # Generate and save summary
            self._process_property_summary(property_data)
            
            # Generate and save review
            self._process_property_review(property_data)

    def _process_property_summary(self, property_data):
        """Generate and save summary for a single property"""
        summary = self.gemini_service.generate_property_summary(property_data)
        if summary:
            PropertySummary.objects.update_or_create(
                property=property_data,
                defaults={'summary': summary}
            )

    def _process_property_review(self, property_data):
        """Generate and save review for a single property"""
        rating, review = self.gemini_service.generate_property_review(property_data)
        if rating and review:
            PropertyReview.objects.update_or_create(
                property=property_data,
                defaults={
                    'rating': rating,
                    'review': review
                }
            )