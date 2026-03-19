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

    def test_create_unit_without_parent(self):
        unit = Unit.objects.create(name="ГШ", unit_type="штаб")

        self.assertEqual(unit.name, "ГШ")
        self.assertIsNone(unit.parent)

    def test_create_unit_with_parent(self):
        company = Unit.objects.create(
            name="3 рота",
            unit_type="рота",
            parent=self.battalion
        )

        self.assertEqual(company.parent, self.battalion)

    def test_sub_units_relationship(self):
        company = Unit.objects.create(
            name="3 рота",
            unit_type="рота",
            parent=self.battalion
        )

        self.assertIn(company, self.battalion.sub_units.all())
        self.assertEqual(self.battalion.sub_units.count(), 1)

    def test_unit_type_stored_correctly(self):
        self.assertEqual(self.battalion.unit_type, "батальйон")

    def test_multiple_children(self):
        company_1 = Unit.objects.create(
            name="1 рота",
            unit_type="рота",
            parent=self.battalion
        )

        company_2 = Unit.objects.create(
            name="2 рота",
            unit_type="рота",
            parent=self.battalion
        )

        company_3 = Unit.objects.create(
            name="3 рота",
            unit_type="рота",
            parent=self.battalion
        )

        self.assertEqual(self.battalion.sub_units.count(), 3)
        self.assertIn(company_1, self.battalion.sub_units.all())
        self.assertIn(company_2, self.battalion.sub_units.all())
        self.assertIn(company_3, self.battalion.sub_units.all())