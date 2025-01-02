# tests/test_commands.py
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch, MagicMock
from property_rewriter.models import ScrapedProperty

class TestRewritePropertiesCommand(TestCase):
    def setUp(self):
        # Clear any existing data
        ScrapedProperty.objects.all().delete()
        
        # Create test property
        self.property = ScrapedProperty.objects.create(
            title='Test Hotel',
            location='Test Location',
            room_type='Suite',
            price=200.0,
            rating=4.5
        )
        # Create StringIO object to capture command output
        self.out = StringIO()


    @patch('property_rewriter.services.property_service.PropertyService.process_all_properties')
    def test_command_successful_execution(self, mock_process):
        """Test successful execution of the command"""
        # Execute command
        call_command('rewrite_properties', stdout=self.out)
        
        # Verify output messages
        output = self.out.getvalue()
        self.assertIn('Starting property rewrite process...', output)
        self.assertIn('Successfully processed all properties', output)
        
        # Verify service method was called
        mock_process.assert_called_once()

    @patch('property_rewriter.services.property_service.PropertyService.process_all_properties')
    def test_command_handles_error(self, mock_process):
        """Test command error handling"""
        # Simulate an error in processing
        mock_process.side_effect = Exception('Test error occurred')
        
        # Execute command
        call_command('rewrite_properties', stdout=self.out)
        
        # Verify error output
        output = self.out.getvalue()
        self.assertIn('Starting property rewrite process...', output)
        self.assertIn('Error processing properties: Test error occurred', output)
        
        # Verify service method was called
        mock_process.assert_called_once()

    