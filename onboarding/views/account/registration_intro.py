from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionAdminStepsMixin
from onboarding.mixins import SuperOrAdminUserRequiredMixin


@class_view_decorator(otp_required)
class OnboardingIntroductionRegistrationView(
    SuperOrAdminUserRequiredMixin, KatIntroductionAdminStepsMixin, TemplateView
):
    """
    Registration introduction
    """

    template_name = "account/step_registration_intro.html"
    current_step = 1
