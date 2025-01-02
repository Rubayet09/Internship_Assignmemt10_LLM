from django.test import TestCase
from django.core.exceptions import ValidationError
from property_rewriter.models import ScrapedProperty, PropertySummary, PropertyReview
from django.utils import timezone

class TestModels(TestCase):
    def setUp(self):
        self.property = ScrapedProperty.objects.create(
            title='Test Hotel',
            location='Test Location',
            room_type='Suite',
            price=200.0,
            rating=4.5
        )

    def test_scraped_property_fields(self):
        self.assertEqual(self.property.title, 'Test Hotel')
        self.assertEqual(self.property.location, 'Test Location')
        self.assertEqual(self.property.room_type, 'Suite')
        self.assertEqual(self.property.price, 200.0)
        self.assertEqual(self.property.rating, 4.5)

        # Test nullable fields
        property_with_nulls = ScrapedProperty.objects.create(
            title='Test Hotel 2',
            location='Test Location 2'
        )
        self.assertIsNone(property_with_nulls.rating)
        self.assertIsNone(property_with_nulls.price)
        self.assertIsNone(property_with_nulls.room_type)

    def test_property_summary_creation(self):
        summary = PropertySummary.objects.create(
            property=self.property,
            summary='Test summary text'
        )
        self.assertEqual(summary.summary, 'Test summary text')
        self.assertIsNotNone(summary.created_at)
        self.assertTrue(isinstance(summary.created_at, timezone.datetime))

    def test_property_review_creation(self):
        review = PropertyReview.objects.create(
            property=self.property,
            rating=4.5,
            review='Test review content'
        )
        self.assertEqual(review.rating, 4.5)
        self.assertEqual(review.review, 'Test review content')
        self.assertIsNotNone(review.created_at)
        self.assertTrue(isinstance(review.created_at, timezone.datetime))

    def test_model_relationships(self):
        # Test one-to-one relationships
        summary = PropertySummary.objects.create(
            property=self.property,
            summary='Test summary'
        )
        review = PropertyReview.objects.create(
            property=self.property,
            rating=4.5,
            review='Test review'
        )

        # Test reverse relationships
        self.assertEqual(self.property.propertysummary, summary)
        self.assertEqual(self.property.propertyreview, review)