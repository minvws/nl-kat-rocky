from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionStepsMixin, OnboardingBreadcrumbsMixin
from onboarding.mixins import RedTeamUserRequiredMixin


@class_view_decorator(otp_required)
class OnboardingChooseReportInfoView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    TemplateView,
):
    template_name = "step_choose_report_info.html"
    current_step = 2


@class_view_decorator(otp_required)
class OnboardingChooseReportTypeView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    TemplateView,
):
    template_name = "step_choose_report_type.html"
    current_step = 2
