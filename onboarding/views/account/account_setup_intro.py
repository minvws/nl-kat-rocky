from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionAdminStepsMixin, SuperOrAdminUserRequiredMixin


@class_view_decorator(otp_required)
class OnboardingAccountSetupIntroView(SuperOrAdminUserRequiredMixin, KatIntroductionAdminStepsMixin, TemplateView):
    template_name = "account/step_account_setup_intro.html"
    current_step = 4
