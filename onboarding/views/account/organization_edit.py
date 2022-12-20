from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from organizations.forms import OrganizationUpdateForm
from onboarding.mixins import KatIntroductionAdminStepsMixin
from organizations.models import Organization
from organizations.mixins import OrganizationsMixin
from onboarding.mixins import SuperOrAdminUserRequiredMixin


@class_view_decorator(otp_required)
class OnboardingOrganizationUpdateView(
    SuperOrAdminUserRequiredMixin,
    KatIntroductionAdminStepsMixin,
    OrganizationsMixin,
    UpdateView,
):
    """
    View to update an existing organization, can only edit name for now.
    """

    model = Organization
    template_name = "account/step_organization_update.html"
    form_class = OrganizationUpdateForm
    current_step = 2

    def get_object(self, queryset=None):
        return self.organization

    def get_success_url(self) -> str:
        return reverse_lazy("step_account_setup_intro", kwargs={"organization_code": self.organization.code})

    def form_valid(self, form):
        org_name = form.cleaned_data["name"]
        self.add_success_notification(org_name)
        return super().form_valid(form)

    def add_success_notification(self, org_name):
        success_message = _("{org_name} succesfully updated.").format(org_name=org_name)
        messages.add_message(self.request, messages.SUCCESS, success_message)
