from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin
from onboarding.forms import OnboardingCreateUserRedTeamerForm

User = get_user_model()


@class_view_decorator(otp_required)
class OnboardingAccountSetupRedTeamerView(
    RegistrationBreadcrumbsMixin,
    OnboardingAccountCreationMixin,
):

    """
    View to create a red team account
    """

    model = User
    template_name = "account/step_redteamer_add.html"
    form_class = OnboardingCreateUserRedTeamerForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("step_account_setup_client")
