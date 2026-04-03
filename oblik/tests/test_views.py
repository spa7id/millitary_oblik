from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from oblik.models import (
    Unit,
    ServiceMember,
    Rank,
    Position,
    AccessProfile,
    Status
)


class IndexViewTest(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('oblik:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oblik/index.html')

    def test_index_shows_counts(self):
        Unit.objects.create(name="Тест", unit_type="рота")
        Rank.objects.create(name="Солдат")

        response = self.client.get(reverse('oblik:index'))

        self.assertIn('num_units', response.context)
        self.assertIn('num_ranks', response.context)
        self.assertEqual(response.context['num_units'], 1)
        self.assertEqual(response.context['num_ranks'], 1)


class UnitsListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='test123'
        )

        self.unit = Unit.objects.create(name="3 рота", unit_type="рота")

        self.rank = Rank.objects.create(name="Майор")

        access_profile = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5
        )

        position = Position.objects.create(
            name="Командир",
            access_profile=access_profile
        )

        status = Status.objects.create(name="Активний")

        ServiceMember.objects.create(
            name="Тест",
            surname="Тестович",
            user=self.user,
            rank=self.rank,
            position=position,
            unit=self.unit,
            status=status
        )

        self.client = Client()

    def test_units_list_requires_login(self):
        response = self.client.get(reverse('oblik:units_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_units_list_with_login(self):
        self.client.login(username='testuser', password='test123')
        response = self.client.get(reverse('oblik:units_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oblik/units_list.html')

    def test_units_list_contains_unit(self):
        self.client.login(username='testuser', password='test123')

        response = self.client.get(reverse('oblik:units_list'))
        self.assertIn(self.unit, response.context['units_list'])
        self.assertContains(response, '3 рота')

    def test_units_list_pagination(self):
        self.client.login(username='testuser', password='test123')

        for i in range(10):
            Unit.objects.create(name=f"Рота {i}", unit_type="рота")

        response = self.client.get(reverse('oblik:units_list'))

        self.assertEqual(len(response.context['units_list']), 8)

    def test_units_list_is_sorted_by_name(self):
        self.client.login(username='testuser', password='test123')

        Unit.objects.create(name="Б рота", unit_type="рота")
        Unit.objects.create(name="А рота", unit_type="рота")

        response = self.client.get(reverse('oblik:units_list'))

        units = list(response.context['units_list'])
        names = [u.name for u in units]
        self.assertEqual(names, sorted(names))


class UnitsDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.hq = Unit.objects.create(name="ГШ", unit_type="штаб")

        cls.battalion = Unit.objects.create(
            name="Батальйон",
            unit_type="батальйон",
            parent=cls.hq
        )

        cls.company = Unit.objects.create(
            name="3 рота",
            unit_type="рота",
            parent=cls.battalion
        )

        cls.officer_user = User.objects.create_user(
            username='officer',
            password='test123'
        )

        officer_profile = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5
        )

        officer_position = Position.objects.create(
            name="Командир",
            access_profile=officer_profile
        )

        rank = Rank.objects.create(name="Майор")
        status = Status.objects.create(name="Активний")

        ServiceMember.objects.create(
            name="Офіцер",
            surname="Командирович",
            user=cls.officer_user,
            rank=rank,
            position=officer_position,
            unit=cls.company,
            status=status
        )

    def setUp(self):
        self.client = Client()

    def test_unit_detail_requires_login(self):
        response = self.client.get(
            reverse('oblik:unit_detail', kwargs={'pk': self.company.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_unit_detail_with_login(self):
        self.client.login(username='officer', password='test123')

        response = self.client.get(
            reverse('oblik:unit_detail', kwargs={'pk': self.company.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oblik/unit_detail.html')

    def test_unit_detail_shows_breadcrumbs(self):
        self.client.login(username='officer', password='test123')

        response = self.client.get(
            reverse('oblik:unit_detail', kwargs={'pk': self.company.pk})
        )

        self.assertIn('breadcrumbs', response.context)
        breadcrumbs = response.context['breadcrumbs']

        self.assertEqual(len(breadcrumbs), 3)
        self.assertEqual(breadcrumbs[0], self.hq)
        self.assertEqual(breadcrumbs[1], self.battalion)
        self.assertEqual(breadcrumbs[2], self.company)

    def test_unit_detail_404_for_nonexistent_unit(self):
        self.client.login(username='officer', password='test123')

        response = self.client.get(
            reverse('oblik:unit_detail', kwargs={'pk': 99999})
        )

        self.assertEqual(response.status_code, 404)

    def test_unit_detail_shows_sub_units(self):
        self.client.login(username='officer', password='test123')

        platoon = Unit.objects.create(
            name="1 взвод",
            unit_type="взвод",
            parent=self.company
        )

        response = self.client.get(
            reverse('oblik:unit_detail', kwargs={'pk': self.company.pk})
        )

        self.assertIn('sub_units', response.context)
        sub_units = list(response.context['sub_units'])
        self.assertIn(platoon, sub_units)

    def test_unit_detail_shows_service_members(self):
        self.client.login(username='officer', password='test123')

        response = self.client.get(
            reverse('oblik:unit_detail', kwargs={'pk': self.company.pk})
        )

        self.assertIn('service_members', response.context)
        self.assertGreater(len(response.context['service_members']), 0)


class ServiceMembersListViewTest(TestCase):
    def setUp(self):
        self.officer_user = User.objects.create_user(
            username='officer',
            password='test123'
        )

        officer_profile = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5
        )

        officer_position = Position.objects.create(
            name="Командир",
            access_profile=officer_profile
        )

        self.unit = Unit.objects.create(name="3 рота", unit_type="рота")
        self.rank = Rank.objects.create(name="Майор")
        self.status = Status.objects.create(name="Активний")

        ServiceMember.objects.create(
            name="Офіцер",
            surname="Командирович",
            user=self.officer_user,
            rank=self.rank,
            position=officer_position,
            unit=self.unit,
            status=self.status
        )

        self.client = Client()

    def test_service_members_list_requires_login(self):
        response = self.client.get(reverse('oblik:service_members_list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_service_members_list_with_login(self):
        self.client.login(username='officer', password='test123')

        response = self.client.get(reverse('oblik:service_members_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oblik/service_members.html')

    def test_officer_sees_all_members(self):
        self.client.login(username='officer', password='test123')

        other_unit = Unit.objects.create(name="4 рота", unit_type="рота")

        soldier_profile = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )

        soldier_position = Position.objects.create(
            name="Стрілець",
            access_profile=soldier_profile
        )

        other_user = User.objects.create_user(
            username='other_soldier',
            password='test123'
        )

        rank = Rank.objects.create(name="Солдат")
        status = Status.objects.create(name="Активний")

        other_member = ServiceMember.objects.create(
            name="Інший",
            surname="Солдатович",
            user=other_user,
            rank=rank,
            position=soldier_position,
            unit=other_unit,
            status=status
        )

        response = self.client.get(reverse('oblik:service_members_list'))

        members = list(response.context['service_members_list'])
        self.assertEqual(len(members), 2)

    def test_soldier_sees_only_own_company(self):
        soldier_user = User.objects.create_user(
            username='soldier',
            password='test123'
        )

        soldier_profile = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )

        soldier_position = Position.objects.create(
            name="Стрілець",
            access_profile=soldier_profile
        )

        rank = Rank.objects.create(name="Солдат")
        status = Status.objects.create(name="Активний")

        soldier_member = ServiceMember.objects.create(
            name="Солдат",
            surname="Іванович",
            user=soldier_user,
            rank=rank,
            position=soldier_position,
            unit=self.unit,
            status=status
        )

        other_unit = Unit.objects.create(name="4 рота", unit_type="рота")

        other_user = User.objects.create_user(
            username='other_soldier',
            password='test123'
        )

        other_member = ServiceMember.objects.create(
            name="Інший",
            surname="Солдатович",
            user=other_user,
            rank=rank,
            position=soldier_position,
            unit=other_unit,
            status=status
        )

        self.client.login(username='soldier', password='test123')

        response = self.client.get(reverse('oblik:service_members_list'))

        members = list(response.context['service_members_list'])

        self.assertEqual(len(members), 2)
        self.assertIn(soldier_member, members)
        self.assertNotIn(other_member, members)

    def test_service_members_sorted_by_surname(self):
        self.client.login(username='officer', password='test123')

        soldier_profile = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )

        position = Position.objects.create(
            name="Стрілець",
            access_profile=soldier_profile
        )

        rank = Rank.objects.create(name="Солдат")
        status = Status.objects.create(name="Активний")

        user1 = User.objects.create_user(username='user1', password='test')
        ServiceMember.objects.create(
            name="Петро",
            surname="Яковенко",
            user=user1,
            rank=rank,
            position=position,
            unit=self.unit,
            status=status
        )

        user2 = User.objects.create_user(username='user2', password='test')
        ServiceMember.objects.create(
            name="Іван",
            surname="Антонович",
            user=user2,
            rank=rank,
            position=position,
            unit=self.unit,
            status=status
        )

        response = self.client.get(reverse('oblik:service_members_list'))

        members = list(response.context['service_members_list'])
        surnames = [m.surname for m in members]

        self.assertEqual(surnames, sorted(surnames))


class RanksListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='test123'
        )

        officer_profile = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5
        )

        position = Position.objects.create(
            name="Командир",
            access_profile=officer_profile
        )

        unit = Unit.objects.create(name="3 рота", unit_type="рота")
        rank = Rank.objects.create(name="Майор")
        status = Status.objects.create(name="Активний")

        ServiceMember.objects.create(
            name="Тест",
            surname="Тестович",
            user=self.user,
            rank=rank,
            position=position,
            unit=unit,
            status=status
        )

        self.client = Client()

    def test_ranks_list_requires_login(self):
        response = self.client.get(reverse('oblik:ranks_list'))

        self.assertEqual(response.status_code, 302)

    def test_ranks_list_with_login(self):
        self.client.login(username='testuser', password='test123')

        response = self.client.get(reverse('oblik:ranks_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oblik/ranks_list.html')

    def test_ranks_list_contains_ranks(self):
        self.client.login(username='testuser', password='test123')

        Rank.objects.create(name="Солдат")
        Rank.objects.create(name="Сержант")

        response = self.client.get(reverse('oblik:ranks_list'))

        ranks = list(response.context['ranks'])
        self.assertEqual(len(ranks), 3)


class PositionsListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='test123'
        )

        officer_profile = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5
        )

        self.position = Position.objects.create(
            name="Командир",
            access_profile=officer_profile
        )

        unit = Unit.objects.create(name="3 рота", unit_type="рота")
        rank = Rank.objects.create(name="Майор")
        status = Status.objects.create(name="Активний")

        ServiceMember.objects.create(
            name="Тест",
            surname="Тестович",
            user=self.user,
            rank=rank,
            position=self.position,
            unit=unit,
            status=status
        )

        self.client = Client()

    def test_positions_list_requires_login(self):
        response = self.client.get(reverse('oblik:positions_list'))

        self.assertEqual(response.status_code, 302)

    def test_positions_list_with_login(self):
        self.client.login(username='testuser', password='test123')

        response = self.client.get(reverse('oblik:positions_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oblik/positions_list.html')


class ServiceMemberDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='test123'
        )

        officer_profile = AccessProfile.objects.create(
            name="Офіцер",
            command_level=5
        )

        position = Position.objects.create(
            name="Командир",
            access_profile=officer_profile
        )

        unit = Unit.objects.create(name="3 рота", unit_type="рота")
        rank = Rank.objects.create(name="Майор")
        status = Status.objects.create(name="Активний")

        self.member = ServiceMember.objects.create(
            name="Тест",
            surname="Тестович",
            user=self.user,
            rank=rank,
            position=position,
            unit=unit,
            status=status
        )

        self.client = Client()

    def test_service_member_detail_requires_login(self):
        response = self.client.get(
            reverse('oblik:service_member_detail',
                    kwargs={'pk': self.member.pk})
        )

        self.assertEqual(response.status_code, 302)

    def test_service_member_detail_with_login(self):
        self.client.login(username='testuser', password='test123')

        response = self.client.get(
            reverse('oblik:service_member_detail',
                    kwargs={'pk': self.member.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oblik/service_member_detail.html')

    def test_service_member_detail_404_for_nonexistent(self):
        self.client.login(username='testuser', password='test123')

        response = self.client.get(
            reverse('oblik:service_member_detail', kwargs={'pk': 99999})
        )

        self.assertEqual(response.status_code, 404)
