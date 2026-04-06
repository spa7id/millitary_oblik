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

class UnitFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "1 взвод",
            "unit_type": "взвод",
            "parent": "",
        }

    def test_valid_form(self):
        form = UnitForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_parent_optional(self):
        data = self.valid_data.copy()
        data["parent"] = ""
        form = UnitForm(data=data)
        self.assertTrue(form.is_valid())

    def test_with_parent_unit(self):
        parent = Unit.objects.create(name="3 рота", unit_type="рота")
        data = self.valid_data.copy()
        data["parent"] = parent.pk
        form = UnitForm(data=data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        form = UnitForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("unit_type", form.errors)

    def test_all_fields_have_form_control_class(self):
        form = UnitForm()
        for field_name, field in form.fields.items():
            self.assertEqual(field.widget.attrs.get("class"), "form-control")

    def test_name_placeholder_set(self):
        form = UnitForm()
        self.assertIn("placeholder", form.fields["name"].widget.attrs)


class UserRegisterFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

    def test_valid_form(self):
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_passwords_dont_match(self):
        data = self.valid_data.copy()
        data["password2"] = "DifferentPass123!"
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = self.valid_data.copy()
        data["email"] = "not-an-email"
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_email_field_present(self):
        form = UserRegisterForm()
        self.assertIn("email", form.fields)

    def test_required_fields_empty(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        for field in ["username", "password1", "password2"]:
            self.assertIn(field, form.errors)