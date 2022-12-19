from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from django.views.generic import TemplateView
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import RedTeamUserRequiredMixin, KatIntroductionStepsMixin, OnboardingBreadcrumbsMixin


@class_view_decorator(otp_required)
class OnboardingSetupScanOOIInfoView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    TemplateView,
):
    template_name = "step_ooi_info.html"
    current_step = 3
