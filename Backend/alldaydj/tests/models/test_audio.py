from alldaydj.models import Cart
from datetime import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase


class CartTestCase(TestCase):
    def test_valid_cuepoints(self):
        # Arrange

        cart = Cart()
        cart.cue_start = 0.0
        cart.cue_intro = 0.1
        cart.cue_outro = 0.2

        # Act

        cart.clean()

        # No assertion as our hope is no exception is raised

    def test_invalid_cuepoints(self):
        # Arrange

        cart = Cart()
        cart.cue_start = 0.2
        cart.cue_intro = 0.1
        cart.cue_outro = 0.0

        # Act and Assert

        with self.assertRaisesMessage(
            ValidationError,
            "['Intro cue of 0.100000 must come after start cue of 0.200000', 'Intro cue of 0.100000 must come before outro cue of 0.000000', 'Start cue of 0.200000 must come before outro cue of 0.000000']",
        ) as context:
            cart.clean()

    def test_valid_times(self):
        # Arrange

        cart = Cart()
        cart.valid_from = datetime(2025, 1, 1, 12, 0, 0)
        cart.valid_until = datetime(2025, 1, 1, 12, 0, 1)
        cart.cue_start = 0.0
        cart.cue_intro = 0.1
        cart.cue_outro = 0.2

        # Act

        cart.clean()

        # No assertion as our hope is no exception is raised

    def test_invalid_times(self):
        # Arrange

        cart = Cart()
        cart.valid_from = datetime(2025, 1, 1, 12, 0, 1)
        cart.valid_until = datetime(2025, 1, 1, 12, 0, 0)
        cart.cue_start = 0.0
        cart.cue_intro = 0.1
        cart.cue_outro = 0.2

        # Act and Assert

        with self.assertRaisesMessage(
            ValidationError,
            "['Valid from date of 2025-01-01 12:00:01 must come before valid until date of 2025-01-01 12:00:00']",
        ) as context:
            cart.clean()
