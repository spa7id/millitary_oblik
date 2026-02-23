from .models import Rank, Position, Status, Unit, ServiceMember, AccessProfile
from django.contrib import admin

admin.site.register(Rank)
admin.site.register(Position)
admin.site.register(Status)
admin.site.register(Unit)
admin.site.register(ServiceMember)
admin.site.register(AccessProfile)
