from datetime import datetime, timezone
from enum import Enum
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from octopoes.models import OOI
from requests.exceptions import RequestException
from katalogus.client import get_katalogus
from katalogus.utils import get_enabled_boefjes_for_ooi_class
from rocky.views import BaseOOIDetailView, OOIRelatedObjectAddView
from tools.forms import ObservedAtForm, PossibleBoefjesFilterForm
from tools.ooi_helpers import format_display
from tools.models import Indemnification, OrganizationMember
from katalogus.views.mixins import BoefjeMixin
from account.mixins import OrganizationsMixin


class PageActions(Enum):
    START_SCAN = "start_scan"


class OOIDetailView(
    BoefjeMixin,
    OOIRelatedObjectAddView,
    BaseOOIDetailView,
    OrganizationsMixin,
):
    template_name = "oois/ooi_detail.html"
    connector_form_class = ObservedAtForm

    def post(self, request, *args, **kwargs):
        if "action" not in self.request.POST:
            return self.get(request, *args, **kwargs)
        self.ooi = self.get_ooi(self.organization.code)
        action_success = self.handle_page_action(request.POST.get("action"))
        if not action_success:
            return self.get(request, *args, **kwargs)

        success_message = (
            "Your scan is running successfully in the background. \n "
            "Results will be added to the object list when they are in. "
            "It may take some time, a refresh of the page may be needed to show the results."
        )
        messages.add_message(request, messages.SUCCESS, success_message)

        return redirect("task_list", organization_code=self.organization.code)

    def handle_page_action(self, action: str) -> bool:
        try:
            if action == PageActions.START_SCAN.value:
                boefje_id = self.request.POST.get("boefje_id")
                ooi_id = self.request.GET.get("ooi_id")

                boefje = get_katalogus(self.organization.code).get_boefje(boefje_id)
                ooi = self.get_single_ooi(self.organization.code, pk=ooi_id)
                self.run_boefje_for_oois(boefje, [ooi], self.api_connector)
                return True

        except RequestException as exception:
            messages.add_message(self.request, messages.ERROR, f"{action} failed: '{exception}'")

    def get_current_ooi(self) -> OOI:
        # self.ooi is already the current state of the OOI
        if self.get_observed_at().date() == datetime.utcnow().date():
            return self.ooi

        try:
            return self.get_ooi(self.organization.code, pk=self.get_ooi_id(), observed_at=datetime.now(timezone.utc))
        except Http404:
            return None

    def get_organizationmember(self):
        return OrganizationMember.objects.get(user=self.request.user, organization=self.organization)

    def get_organization_indemnification(self):
        return Indemnification.objects.filter(organization=self.organization).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_form = PossibleBoefjesFilterForm(self.request.GET)

        # List from katalogus
        boefjes = get_enabled_boefjes_for_ooi_class(self.ooi.__class__, self.organization)

        if boefjes:
            context["enabled_boefjes_available"] = True

        # Filter boefjes on scan level <= OOI clearance level when not "show all"
        # or when not "acknowledged clearance level > 0"
        member = self.get_organizationmember()
        if (
            (filter_form.is_valid() and not filter_form.cleaned_data["show_all"])
            or member.acknowledged_clearance_level <= 0
            or self.get_organization_indemnification()
        ):
            boefjes = [boefje for boefje in boefjes if boefje.scan_level.value <= self.ooi.scan_profile.level]

        context["boefjes"] = boefjes
        context["ooi"] = self.ooi

        declarations, observations, inferences = self.get_origins(
            self.ooi.reference, self.get_observed_at(), self.organization
        )
        context["declarations"] = declarations
        context["observations"] = observations
        context["inferences"] = inferences
        context["member"] = self.get_organizationmember()
        context["object_details"] = format_display(self.get_ooi_properties(self.ooi))
        context["ooi_types"] = self.get_ooi_types_input_values(self.ooi)
        context["observed_at_form"] = self.get_connector_form()
        context["observed_at"] = self.get_observed_at()
        context["ooi_past_due"] = context["observed_at"].date() < datetime.utcnow().date()
        context["related"] = self.get_related_objects()
        context["ooi_current"] = self.get_current_ooi()
        context["findings_severity_summary"] = self.findings_severity_summary()
        context["severity_summary_totals"] = self.get_findings_severity_totals()
        context["possible_boefjes_filter_form"] = filter_form
        context["organization_indemnification"] = self.get_organization_indemnification()

        return context
