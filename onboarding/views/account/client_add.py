from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth import get_user_model
from onboarding.forms import OnboardingCreateUserClientForm
from onboarding.mixins import RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin


User = get_user_model()


@class_view_decorator(otp_required)
class OnboardingAccountSetupClientView(RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin):
    """
    View to create a client account
    """

    model = User
    template_name = "account/step_client_add.html"
    form_class = OnboardingCreateUserClientForm
    success_url = reverse_lazy("crisis_room")
