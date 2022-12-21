from django.contrib import messages
from django.urls.base import reverse
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from rocky.view_helpers import get_ooi_url
from onboarding.mixins import RedTeamUserRequiredMixin, KatIntroductionStepsMixin, OnboardingBreadcrumbsMixin
from onboarding.forms import OnboardingSetClearanceLevelForm
from organizations.mixins import OrganizationsMixin


@class_view_decorator(otp_required)
class OnboardingSetClearanceLevelView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    OrganizationsMixin,
    FormView,
):
    template_name = "step_set_clearance_level.html"
    form_class = OnboardingSetClearanceLevelForm
    current_step = 3
    initial = {"level": 2}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["boefjes"] = self.get_boefjes_tiles()
        return context

    def get_success_url(self, **kwargs):
        return get_ooi_url(
            "step_setup_scan_select_plugins",
            self.request.GET.get("ooi_id"),
            kwargs={"organization_code": self.organization.code},
        )

    def form_valid(self, form):
        self.request.session["clearance_level"] = form.data["level"]
        self.add_success_notification()
        return super().form_valid(form)

    def add_success_notification(self):
        success_message = _("Clearance level has been set")
        messages.add_message(self.request, messages.SUCCESS, success_message)

    def get_boefje_cover_img(self, boefje_id):
        return reverse("plugin_cover", kwargs={"plugin_id": boefje_id})

    def get_boefjes_tiles(self):
        tiles = [
            {
                "tile_image": self.get_boefje_cover_img("dns_zone"),
                "scan_level": "l1",
                "name": "DNS-Zone",
                "description": "Fetch the parent DNS zone of a hostname",
            },
            {
                "tile_image": self.get_boefje_cover_img("fierce"),
                "scan_level": "l3",
                "name": "Fierce",
                "description": "Finds subdomains by brute force",
            },
        ]
        return tiles
