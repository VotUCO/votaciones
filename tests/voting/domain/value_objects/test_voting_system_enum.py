from django.test import TestCase

from src.voting.domain.value_objects.voting_system_enum import VotingSystemEnum

class VotingEnumTest(TestCase):
    def test_create_voting(self):
        enum = VotingSystemEnum("scoring")
        self.assertEqual(enum, VotingSystemEnum.SCORING)

    def test_error_status(self):
        try:
            VotingSystemEnum("example_error")
        except Exception as e:
            self.assertIsNot(e, VotingSystemEnum)