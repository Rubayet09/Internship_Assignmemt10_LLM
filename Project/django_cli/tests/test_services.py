# test_services.py
from django.test import TestCase
from unittest.mock import patch, MagicMock
from property_rewriter.services.property_service import PropertyService
from property_rewriter.models import ScrapedProperty, PropertySummary, PropertyReview

class TestPropertyService(TestCase):
    def setUp(self):
        # Clear any existing data
        ScrapedProperty.objects.all().delete()
        
        self.service = PropertyService()
        self.property = ScrapedProperty.objects.create(
            title='Test Hotel',
            location='Test Location',
            room_type='Suite',
            price=200.0,
            rating=4.5
        )

    @patch('property_rewriter.services.gemini_service.GeminiService.generate_property_summary')
    def test_process_property_summary(self, mock_summary):
        # Test successful summary processing
        mock_summary.return_value = "Test summary"
        self.service._process_property_summary(self.property)
        summary = PropertySummary.objects.get(property=self.property)
        self.assertEqual(summary.summary, "Test summary")

        # Test summary update
        mock_summary.return_value = "Updated summary"
        self.service._process_property_summary(self.property)
        summary.refresh_from_db()
        self.assertEqual(summary.summary, "Updated summary")

        # Test failed summary generation
        mock_summary.return_value = None
        self.service._process_property_summary(self.property)
        summary.refresh_from_db()
        self.assertEqual(summary.summary, "Updated summary")  # Should remain unchanged

    @patch('property_rewriter.services.gemini_service.GeminiService.generate_property_review')
    def test_process_property_review(self, mock_review):
        # Test successful review processing
        mock_review.return_value = (4.5, "Test review")
        self.service._process_property_review(self.property)
        review = PropertyReview.objects.get(property=self.property)
        self.assertEqual(review.rating, 4.5)
        self.assertEqual(review.review, "Test review")

        # Test review update
        mock_review.return_value = (4.0, "Updated review")
        self.service._process_property_review(self.property)
        review.refresh_from_db()
        self.assertEqual(review.rating, 4.0)
        self.assertEqual(review.review, "Updated review")

        # Test failed review generation
        mock_review.return_value = (None, None)
        self.service._process_property_review(self.property)
        review.refresh_from_db()
        self.assertEqual(review.rating, 4.0)  # Should remain unchanged
        self.assertEqual(review.review, "Updated review")  # Should remain unchanged

    @patch('property_rewriter.services.property_service.PropertyService._process_property_summary')
    @patch('property_rewriter.services.property_service.PropertyService._process_property_review')
    def test_process_all_properties(self, mock_review, mock_summary):
        # Create a second test property
        property2 = ScrapedProperty.objects.create(
            title='Test Hotel 2',
            location='Test Location 2',
            room_type='Double',
            price=150.0,
            rating=4.0
        )

        # Get the count of properties to verify the exact number of calls expected
        expected_calls = ScrapedProperty.objects.count()
        
        # Process all properties
        self.service.process_all_properties()
        
        # Verify both summary and review were processed for all properties
        self.assertEqual(mock_summary.call_count, expected_calls)
        self.assertEqual(mock_review.call_count, expected_calls)

        # Verify that each property was processed
        for prop in [self.property, property2]:
            mock_summary.assert_any_call(prop)
            mock_review.assert_any_call(prop)