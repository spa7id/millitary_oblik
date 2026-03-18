from django.test import TestCase
from oblik.models import Unit, ServiceMember, Rank, Position, AccessProfile
from django.contrib.auth.models import User
from datetime import date


class UnitModelTest(TestCase):
    def setUp(self):
        self.battalion = Unit.objects.create(
            name="1 батальйон",
            unit_type="батальйон"
        )

    def test_str_method(self):
        self.assertEqual(str(self.battalion), "1 батальйон")