from django.core.management.base import BaseCommand
from property_rewriter.services.property_service import PropertyService

class Command(BaseCommand):
    help = 'Rewrite property information using Gemini AI'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting property rewrite process...')
        
        service = PropertyService()
        try:
            service.process_all_properties()
            self.stdout.write(self.style.SUCCESS('Successfully processed all properties'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing properties: {e}'))