from django.test import TestCase
from datetime import date, timedelta
from oblik.forms import ServiceMemberForm, UnitForm, UserRegisterForm
from oblik.models import Rank, Position, Unit, Status, AccessProfile


class ServiceMemberFormTest(TestCase):
    def setUp(self):
        self.access_profile = AccessProfile.objects.create(
            name="Солдат",
            command_level=1
        )
        self.position = Position.objects.create(
            name="Стрілець",
            access_profile=self.access_profile
        )
        self.rank = Rank.objects.create(name="Рядовий")
        self.unit = Unit.objects.create(name="1 взвод", unit_type="взвод")
        self.status = Status.objects.create(name="Активний")

        self.valid_data = {
            "name": "Іван",
            "surname": "Петренко",
            "middle_name": "Васильович",
            "call_sign": "Сокіл",
            "birth_date": "1995-05-15",
            "rank": self.rank.pk,
            "position": self.position.pk,
            "unit": self.unit.pk,
            "status": self.status.pk,
        }

    def test_valid_form(self):
        form = ServiceMemberForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_birth_date_in_future_is_invalid(self):
        future_date = date.today() + timedelta(days=1)
        data = self.valid_data.copy()
        data["birth_date"] = future_date.strftime("%Y-%m-%d")
        form = ServiceMemberForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("birth_date", form.errors)

    def test_birth_date_today_is_valid(self):
        data = self.valid_data.copy()
        data["birth_date"] = date.today().strftime("%Y-%m-%d")
        form = ServiceMemberForm(data=data)
        self.assertTrue(form.is_valid())

    def test_birth_date_empty_is_valid(self):
        data = self.valid_data.copy()
        data["birth_date"] = ""
        form = ServiceMemberForm(data=data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        form = ServiceMemberForm(data={})
        self.assertFalse(form.is_valid())
        for field in ["name", "surname", "rank", "position", "unit", "status"]:
            self.assertIn(field, form.errors)

    def test_all_fields_have_form_control_class(self):
        form = ServiceMemberForm()
        for field_name, field in form.fields.items():
            self.assertEqual(field.widget.attrs.get("class"), "form-control")

    def test_user_field_excluded(self):
        form = ServiceMemberForm()
        self.assertNotIn("user", form.fields)