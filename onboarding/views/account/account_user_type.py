from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionAdminStepsMixin
from organizations.mixins import OrganizationsMixin


@class_view_decorator(otp_required)
class OnboardingChooseUserTypeView(KatIntroductionAdminStepsMixin, OrganizationsMixin, TemplateView):
    current_step = 4
    template_name = "account/step_account_user_type.html"
