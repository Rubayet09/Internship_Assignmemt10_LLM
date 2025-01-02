from django.test import TestCase
from unittest.mock import patch, MagicMock
from property_rewriter.services.gemini_service import GeminiService
from property_rewriter.models import ScrapedProperty
import json

class TestGeminiIntegration(TestCase):
    def setUp(self):
        self.gemini_service = GeminiService()
        self.test_property = ScrapedProperty.objects.create(
            title='Test Hotel',
            location='Test Location',
            room_type='Suite',
            price=200.0,
            rating=4.5
        )

    @patch('requests.post')
    def test_successful_api_call(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Test content'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        result = self.gemini_service.generate_content("Test prompt")
        self.assertEqual(result, 'Test content')
        self.assertTrue(mock_post.called)

    @patch('requests.post')
    def test_api_error_handling(self, mock_post):
        # Test network error
        mock_post.side_effect = Exception("Network error")
        result = self.gemini_service.generate_content("Test prompt")
        self.assertIsNone(result)

        # Test empty response
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_post.side_effect = None
        mock_post.return_value = mock_response
        result = self.gemini_service.generate_content("Test prompt")
        self.assertIsNone(result)

    @patch('property_rewriter.services.gemini_service.GeminiService.generate_content')
    def test_property_summary_generation(self, mock_generate):
        # Test successful summary generation
        mock_generate.return_value = "Test summary description"
        result = self.gemini_service.generate_property_summary(self.test_property)
        self.assertEqual(result, "Test summary description")

        # Test failed summary generation
        mock_generate.return_value = None
        result = self.gemini_service.generate_property_summary(self.test_property)
        self.assertIsNone(result)

    @patch('property_rewriter.services.gemini_service.GeminiService.generate_content')
    def test_property_review_generation(self, mock_generate):
        # Test successful review generation
        valid_json = '{"rating": 4.5, "review": "Great hotel!"}'
        mock_generate.return_value = valid_json
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertEqual(rating, 4.5)
        self.assertEqual(review, "Great hotel!")

        # Test invalid JSON response
        mock_generate.return_value = "Invalid JSON"
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertIsNone(rating)
        self.assertIsNone(review)

        # Test invalid rating range
        mock_generate.return_value = '{"rating": 6.0, "review": "Test"}'
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertIsNone(rating)
        self.assertIsNone(review)

        # Test missing fields
        mock_generate.return_value = '{"rating": 4.5}'
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertIsNone(rating)
        self.assertIsNone(review)

    @patch('property_rewriter.services.gemini_service.GeminiService.generate_content')
    def test_property_review_edge_cases(self, mock_generate):
        # Test None response
        mock_generate.return_value = None
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertIsNone(rating)
        self.assertIsNone(review)

        # Test response with no JSON content
        mock_generate.return_value = "No JSON content here"
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertIsNone(rating)
        self.assertIsNone(review)

        # Test response with invalid JSON format
        mock_generate.return_value = '{"rating": "not_a_number", "review": "Test"}'
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertIsNone(rating)
        self.assertIsNone(review)

        # Test response with JSON embedded in text
        mock_generate.return_value = 'Here is the review: {"rating": 4.5, "review": "Test review"} Thank you!'
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertEqual(rating, 4.5)
        self.assertEqual(review, "Test review")

        # Test empty string response
        mock_generate.return_value = ''
        rating, review = self.gemini_service.generate_property_review(self.test_property)
        self.assertIsNone(rating)
        self.assertIsNone(review)