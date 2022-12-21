from datetime import datetime, timezone
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from octopoes.models import DeclaredScanProfile
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionStepsMixin
from katalogus.client import get_katalogus
from oois.mixins import SingleOOITreeMixin
from onboarding.mixins import RedTeamUserRequiredMixin, OnboardingBreadcrumbsMixin
from rocky.view_helpers import get_ooi_url
from organizations.mixins import OrganizationsMixin


@class_view_decorator(otp_required)
class OnboardingSetupScanOOIDetailView(
    RedTeamUserRequiredMixin,
    SingleOOITreeMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    OrganizationsMixin,
    TemplateView,
):
    template_name = "step_ooi_detail.html"
    current_step = 3

    def get_ooi_id(self) -> str:
        if "ooi_id" in self.request.session:
            return self.request.session["ooi_id"]
        return super().get_ooi_id()

    def get(self, request, *args, **kwargs):
        self.api_connector = self.get_api_connector(self.organization.code)
        self.ooi = self.get_ooi(self.organization.code)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_clearance_level()
        self.enable_selected_boefjes()
        return redirect(get_ooi_url("step_report", self.get_ooi_id(), organization_code=self.organization.code))

    def set_clearance_level(self):
        self.api_connector = self.get_api_connector(self.organization.code)
        ooi = self.get_ooi(self.organization.code)
        self.api_connector.save_scan_profile(
            DeclaredScanProfile(reference=ooi.reference, level=self.request.session["clearance_level"]),
            valid_time=datetime.now(timezone.utc),
        )

    def enable_selected_boefjes(self) -> None:
        if not self.request.session.get("selected_boefjes"):
            return
        for boefje_id in self.request.session["selected_boefjes"]:
            get_katalogus(self.organization.code).enable_boefje(boefje_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ooi"] = self.ooi
        return context
