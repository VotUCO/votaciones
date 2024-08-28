from django.test import TestCase

from src.voting.domain.value_objects.status_enum import StatusEnum


class StatusEnumTest(TestCase):
    def test_create_status(self):
        enum = StatusEnum("draft")
        self.assertEqual(enum, StatusEnum.DRAFT)

    def test_error_status(self):
        try:
            StatusEnum("example_error")
        except Exception as e:
            self.assertIsNot(e, StatusEnum)