from django.contrib.auth.models import User
from django.db import models


class Rank(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AccessProfile(models.Model):

    name = models.CharField(max_length=100)

    can_view_subordinates = models.BooleanField(default=False)
    can_edit_subordinates = models.BooleanField(default=False)
    can_add_personnel = models.BooleanField(default=False)
    can_delete_personnel = models.BooleanField(default=False)

    command_level = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=50)

    access_profile = models.ForeignKey(
        AccessProfile,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sub_units",
    )

    def __str__(self):
        return f"{self.unit_type}: {self.name}"


class ServiceMember(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_member"
    )

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    call_sign = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)

    rank = models.ForeignKey(
        Rank, on_delete=models.PROTECT, related_name="service_members"
    )

    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="service_members"
    )

    unit = models.ForeignKey(
        Unit, on_delete=models.PROTECT, related_name="service_members"
    )

    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, related_name="service_members"
    )

    def __str__(self):
        return f"{self.surname} {self.name} ({self.call_sign})"

