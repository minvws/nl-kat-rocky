from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth import get_user_model
from onboarding.mixins import RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin
from onboarding.forms import OnboardingCreateUserAdminForm
from organizations.mixins import OrganizationsMixin

User = get_user_model()


@class_view_decorator(otp_required)
class OnboardingAccountSetupAdminView(RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin):
    """
    View to create a new admin account
    """

    model = User
    template_name = "account/step_admin_add.html"
    form_class = OnboardingCreateUserAdminForm

    def get_success_url(self) -> str:
        return reverse_lazy("step_account_setup_red_teamer", kwargs={"organization_code": self.organization.code})
