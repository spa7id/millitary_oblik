from django.test import TestCase
from oblik.models import (Unit, ServiceMember, Rank, Position, AccessProfile,
                          Status)
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


class RankModelTest(TestCase):
    def test_create_rank(self):
        rank = Rank.objects.create(name="Солдат")
        self.assertEqual(rank.name, "Солдат")

    def test_str_method_returns_name(self):
        rank = Rank.objects.create(name="Сержант")

        self.assertEqual(str(rank), "Сержант")

    def test_rank_name_is_stored_correctly(self):
        rank = Rank.objects.create(name="Лейтенант")
        rank_from_db = Rank.objects.get(pk=rank.pk)

        self.assertEqual(rank_from_db.name, "Лейтенант")

    def test_can_create_multiple_ranks(self):
        rank_1 = Rank.objects.create(name="Солдат")
        rank_2 = Rank.objects.create(name="Сержант")
        rank_3 = Rank.objects.create(name="Лейтенант")

        self.assertEqual(Rank.objects.count(), 3)

    def test_rank_name_max_length(self):
        long_name = "А" * 50
        rank = Rank.objects.create(name=long_name)

        self.assertEqual(len(rank.name), 50)


class PositionModelTest(TestCase):
    def setUp(self):
        self.access_profile = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )

    def test_create_position(self):
        position = Position.objects.create(
            name="Стрілець",
            access_profile=self.access_profile
        )

        self.assertEqual(position.name, "Стрілець")
        self.assertEqual(position.access_profile, self.access_profile)

    def test_str_method(self):
        position = Position.objects.create(
            name="Командир відділення",
            access_profile=self.access_profile
        )

        self.assertIn("Командир відділення", str(position))

    def test_position_to_access_profile_relationship(self):
        position = Position.objects.create(
            name="Стрілець",
            access_profile=self.access_profile
        )

        self.assertEqual(position.access_profile.name, "Солдат")
        self.assertEqual(position.access_profile.command_level, 1)


class AccessProfileModelTest(TestCase):
    def test_create_access_profile(self):
        profile = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5,
        )

        self.assertEqual(profile.name, "Офіцер")
        self.assertEqual(profile.command_level, 5)

    def test_str_method(self):
        profile = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )

        self.assertIn("Солдат", str(profile))

    def test_command_level_determines_access(self):
        soldier = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )

        officer = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5
        )

        self.assertLess(soldier.command_level, officer.command_level)
        self.assertTrue(officer.command_level >= 4)

class ServiceMemberModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='test123'
        )

        self.unit = Unit.objects.create(name="3 рота", unit_type="рота")

        self.rank = Rank.objects.create(name="Солдат")

        access_profile = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )

        self.position = Position.objects.create(
            name="Стрілець",
            access_profile=access_profile
        )

        self.status = Status.objects.create(
            name="Активний"
        )

    def test_create_service_member_with_required_fields(self):
        member = ServiceMember.objects.create(
            name="Іван",
            surname="Коваль",
            user=self.user,
            rank=self.rank,
            position=self.position,
            unit=self.unit,
            status = self.status
        )

        self.assertEqual(member.name, "Іван")
        self.assertEqual(member.surname, "Коваль")

    def test_create_service_member_with_all_fields(self):
        member = ServiceMember.objects.create(
            name="Іван",
            surname="Коваль",
            middle_name="Петрович",
            call_sign="Вовк",
            birth_date=date(2000, 1, 1),
            user=self.user,
            rank=self.rank,
            position=self.position,
            unit=self.unit,
            status = self.status,
        )

        self.assertEqual(member.middle_name, "Петрович")
        self.assertEqual(member.call_sign, "Вовк")
        self.assertEqual(member.birth_date, date(2000, 1, 1))

    def test_service_member_str_contains_name(self):
        member = ServiceMember.objects.create(
            name="Іван",
            surname="Коваль",
            user=self.user,
            rank=self.rank,
            position=self.position,
            unit=self.unit,
            status = self.status
        )

        result = str(member)

        self.assertIn("Іван", result)
        self.assertIn("Коваль", result)

    def test_user_to_service_member_relationship(self):
        member = ServiceMember.objects.create(
            name="Іван",
            surname="Коваль",
            user=self.user,
            rank=self.rank,
            position=self.position,
            unit=self.unit,
            status=self.status
        )

        self.assertEqual(member.user, self.user)

        self.assertEqual(self.user.service_member, member)

    def test_service_member_has_correct_relationships(self):
        member = ServiceMember.objects.create(
            name="Іван",
            surname="Коваль",
            user=self.user,
            rank=self.rank,
            position=self.position,
            unit=self.unit,
            status=self.status
        )

        self.assertEqual(member.rank.name, "Солдат")
        self.assertEqual(member.position.name, "Стрілець")
        self.assertEqual(member.unit.name, "3 рота")
        self.assertEqual(
            member.position.access_profile.command_level,
            1
        )