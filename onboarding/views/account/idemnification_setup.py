from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionAdminStepsMixin
from onboarding.mixins import SuperOrAdminUserRequiredMixin
from organizations.views.indemnification_add import IndemnificationAddView


@class_view_decorator(otp_required)
class OnboardingIndemnificationSetupView(
    SuperOrAdminUserRequiredMixin,
    KatIntroductionAdminStepsMixin,
    IndemnificationAddView,
):
    current_step = 4
    template_name = "account/step_indemnification_setup.html"

    def get_success_url(self) -> str:
        return reverse_lazy("step_account_setup_intro", kwargs={"organization_code": self.organization.code})
