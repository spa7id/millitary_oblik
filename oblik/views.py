from django.contrib.auth import login
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.http import HttpRequest, HttpResponse

from django.shortcuts import render, redirect
from .models import ServiceMember, Rank, Unit, Position
from .forms import ServiceMemberForm, UserRegisterForm
#from millitary_oblik.forms import ServiceMemberCreationForm
from .mixins import (
    CanAddPersonnelMixin,
    CanEditPersonnelMixin,
    CanDeletePersonnelMixin
)

def index(request: HttpRequest) -> HttpResponse:
    num_soldiers = ServiceMember.objects.count()
    num_ranks = Rank.objects.count()
    num_units = Unit.objects.count()
    context = {
        "num_soldiers": num_soldiers,
        "num_ranks": num_ranks,
        "num_units": num_units,
    }
    return render(request, "oblik/index.html", context=context)


class Units_List_View(LoginRequiredMixin, generic.ListView):
    model = Unit
    template_name = "oblik/units_list.html"
    context_object_name = "units_list"


class Service_Members_List_View(LoginRequiredMixin, generic.ListView):
    model = ServiceMember
    template_name = "oblik/service_members.html"
    context_object_name = "service_members_list"
    #paginate_by = 4

    def find_unit_by_type(self, start_unit, unit_type):
        """Знайти підрозділ певного типу, рухаючись вгору"""
        current = start_unit

        if current.unit_type == unit_type:
            return current

        while current.parent:
            current = current.parent
            if current.unit_type == unit_type:
                return current

        return None

    def get_queryset(self):
        user = self.request.user
        my_command_level = user.service_member.position.access_profile.command_level
        print(f"Command level: {my_command_level}")

        if my_command_level >= 4:
            print("Офіцер - показую всіх!")
            queryset = ServiceMember.objects.select_related(
                "rank", "position", "unit", "status",
            )
            return queryset
        else:
            print("Солдат - фільтрація по роті!")

            my_unit = user.service_member.unit
            print(f"Мій підрозділ: {my_unit.name}")

            my_company = self.find_unit_by_type(my_unit, "рота")
            print(
                f"Моя рота: {my_company.name if my_company else 'Не знайдено'}")

            queryset = ServiceMember.objects.select_related(
                "rank", "position", "unit", "status",
            ).filter(unit=my_company)
            return queryset


class Service_Member_Update_View(LoginRequiredMixin, generic.UpdateView):
    model = ServiceMember
    fields = "__all__"
    success_url = reverse_lazy("oblik:service_members_list")
    template_name = "oblik/service_member_update_form.html"

class Service_Member_Delete_View(LoginRequiredMixin, generic.DeleteView):
    model = ServiceMember
    template_name = "oblik/service_member_confirm_delete.html"
    success_url = reverse_lazy("oblik:units_list")
    context_object_name = "service_member"

class Service_Members_Detail_View(LoginRequiredMixin, generic.DetailView):
    model = ServiceMember
    template_name = "oblik/service_member_detail.html"
    context_object_name = "service_member"


class ServiceManCreateView(CanAddPersonnelMixin, generic.CreateView):
    model = ServiceMember
    form_class = ServiceMemberForm
    success_url = reverse_lazy("oblik:service_members_list")
    template_name = "oblik/service_form_create.html"


class Units_List_Create_View(LoginRequiredMixin, generic.CreateView):
    model = Unit
    fields = "__all__"
    success_url = reverse_lazy("oblik:units_list")
    template_name = "oblik/unit_form.html"

class Units_Update_View(LoginRequiredMixin, generic.UpdateView):
    model = Unit
    fields = "__all__"
    success_url = reverse_lazy("oblik:units_list")
    template_name = "oblik/unit_form.html"

class Units_Delete_View(LoginRequiredMixin, generic.DeleteView):
    model = Unit
    template_name = "oblik/unit_form_confirm_delete.html"
    success_url = reverse_lazy("oblik:units_list")

class Ranks_List_View(LoginRequiredMixin, generic.ListView):
    model = Rank
    template_name = "oblik/ranks_list.html"
    context_object_name = "ranks"

class Rank_Create_View(LoginRequiredMixin, generic.CreateView):
    model = Rank
    fields = "__all__"
    success_url = reverse_lazy("oblik:ranks_list")
    template_name = "oblik/rank_create_form.html"

class Rank_Update_View(LoginRequiredMixin, generic.UpdateView):
    model = Rank
    fields = "__all__"
    success_url = reverse_lazy("oblik:ranks_list")
    template_name = "oblik/rank_form_update.html"

class Rank_Delete_View(LoginRequiredMixin, generic.DeleteView):
    model = Rank
    template_name = "oblik/rank_form_confirm_delete.html"
    success_url = reverse_lazy("oblik:ranks_list")
    context_object_name = "rank_delete"

class Positions_List_View(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "oblik/positions_list.html"
    context_object_name = "positions"

class Position_Create_View(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("oblik:positions_list")
    template_name = "oblik/position_create_form.html"

class Position_Update_View(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("oblik:positions_list")
    template_name = "oblik/position_form_update.html"

class Position_Delete_View(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "oblik/position_form_confirm_delete.html"
    success_url = reverse_lazy("oblik:positions_list")
    context_object_name = "position"

def register_view(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        sm_form = ServiceMemberForm(request.POST)

        if user_form.is_valid() and sm_form.is_valid():
            user = user_form.save()

            service_member = sm_form.save(commit=False)
            service_member.user = user
            service_member.save()

            login(request, user)

            return redirect("oblik:index")
    else:
        user_form = UserRegisterForm()
        sm_form = ServiceMemberForm()

    return render(
        request,
        "registration/register.html",
        {
            "user_form": user_form,
            "sm_form": sm_form,
        },
    )


# class Create_User_View(LoginRequiredMixin, generic.CreateView):
#     fields = "__all__"
#     form_class = ServiceMemberCreationForm

def test_session_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "<h1> TEST SESSION </h1>"
        f"<h4> Session data {request.session['Rank']}</h4>"
    )

