from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


class CanAddPersonnelMixin(UserPassesTestMixin):
    """Перевірка чи може користувач додавати персонал"""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        try:
            service_member = self.request.user.service_member
            return service_member.position.access_profile.can_add_personnel
        except:
            return False

    def handle_no_permission(self):
        messages.error(self.request,
                       "У вас немає прав для додавання персоналу")
        return redirect("oblik:index")


class CanEditPersonnelMixin(UserPassesTestMixin):
    """Перевірка чи може користувач редагувати персонал"""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        try:
            service_member = self.request.user.service_member
            return service_member.position.access_profile.can_edit_subordinates
        except:
            return False

    def handle_no_permission(self):
        messages.error(self.request,
                       "У вас немає прав для редагування персоналу")
        return redirect("oblik:index")


class CanDeletePersonnelMixin(UserPassesTestMixin):
    """Перевірка чи може користувач видаляти персонал"""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        try:
            service_member = self.request.user.service_member
            return service_member.position.access_profile.can_delete_personnel
        except:
            return False

    def handle_no_permission(self):
        messages.error(self.request,
                       "У вас немає прав для видалення персоналу")
        return redirect("oblik:index")