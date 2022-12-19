from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth import get_user_model
from onboarding.mixins import KatIntroductionStepsMixin
from rocky.user_helpers import is_red_team
from onboarding.mixins import RedTeamUserRequiredMixin
from onboarding.mixins import OnboardingBreadcrumbsMixin

User = get_user_model()


def index(request):
    if request.user.is_superuser:
        return redirect("step_introduction_registration")
    if is_red_team(request.user):
        return redirect("step_introduction")
    return redirect("crisis_room")


@class_view_decorator(otp_required)
class OnboardingIntroductionView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    TemplateView,
):
    template_name = "step_introduction.html"
    current_step = 1
