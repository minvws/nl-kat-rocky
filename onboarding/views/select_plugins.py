from typing import Type, Dict, Any
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionStepsMixin, OnboardingBreadcrumbsMixin
from katalogus.forms import SelectBoefjeForm
from onboarding.mixins import RedTeamUserRequiredMixin
from rocky.view_helpers import get_ooi_url
from oois.views import Report, DNSReport


@class_view_decorator(otp_required)
class OnboardingSetupScanSelectPluginsView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    TemplateView,
):
    template_name = "step_select_plugins.html"
    current_step = 3
    report: Type[Report] = DNSReport

    def get_form(self):
        boefjes = self.report.get_boefjes(self.request.active_organization)
        kwargs = {
            "boefjes": [
                boefje
                for boefje in boefjes
                if boefje["boefje"].scan_level <= int(self.request.session["clearance_level"])
            ],
            "initial": {"boefje": [item["id"] for item in boefjes if item.get("required", False)]},
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                }
            )

        return SelectBoefjeForm(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if "boefje" in request.POST:
                data = form.cleaned_data
                request.session["selected_boefjes"] = data
            return redirect(get_ooi_url("step_setup_scan_ooi_detail", self.request.GET.get("ooi_id")))
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context["xxxboefjes"] = self.report.get_boefjes()
        context["select_boefjes_form"] = self.get_form()
        return context
