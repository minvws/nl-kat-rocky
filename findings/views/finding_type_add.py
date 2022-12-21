from datetime import datetime, timezone
from django.shortcuts import redirect
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from django_otp.decorators import otp_required
from octopoes.api.models import Declaration
from octopoes.models.ooi.findings import KATFindingType
from two_factor.views.utils import class_view_decorator
from oois.mixins import OctopoesMixin
from oois.models import OOIInformation
from findings.forms import FindingTypeAddForm
from rocky.view_helpers import get_ooi_url
from organizations.mixins import OrganizationsMixin


@class_view_decorator(otp_required)
class FindingTypeAddView(OctopoesMixin, OrganizationsMixin, FormView):
    template_name = "finding_type_add.html"
    form_class = FindingTypeAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [
            {"url": reverse("finding_list"), "text": _("Findings")},
            {"url": reverse("finding_type_add"), "text": _("Add finding type")},
        ]

        return context

    def form_valid(self, form):
        self.api_connector = self.get_api_connector(self.organization.code)
        form_data = form.cleaned_data
        # set data
        finding_type = KATFindingType(id=form_data["id"])
        info, created = OOIInformation.objects.get_or_create(id=f'KATFindingType|{form_data["id"]}')
        info.data = {
            "title": form_data["title"],
            "description": form_data["description"],
            "risk": form_data["risk"],
            "solution": form_data["solution"],
            "references": form_data["references"],
            "impact_description": form_data["impact_description"],
            "solution_chance": form_data["solution_chance"],
            "solution_impact": form_data["solution_impact"],
            "solution_effort": form_data["solution_effort"],
        }

        info.save()

        self.api_connector.save_declaration(Declaration(ooi=finding_type, valid_time=datetime.now(timezone.utc)))

        return redirect(get_ooi_url("ooi_detail", finding_type.primary_key))
