from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from organizations.forms import OrganizationForm
from onboarding.mixins import KatIntroductionAdminStepsMixin
from organizations.models import Organization
from onboarding.mixins import SuperOrAdminUserRequiredMixin


@class_view_decorator(otp_required)
class OnboardingOrganizationSetupView(
    SuperOrAdminUserRequiredMixin,
    KatIntroductionAdminStepsMixin,
    CreateView,
):
    """
    View to create a new organization
    """

    model = Organization
    template_name = "account/step_organization_setup.html"
    form_class = OrganizationForm
    current_step = 2
    organization = Organization.objects.first()

    def get(self, request, *args, **kwargs):
        if self.organization:
            return redirect(reverse("step_organization_update", kwargs={"organization_code": self.organization.code}))
        return super().get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy("step_account_setup_intro", kwargs={"organization_code": self.organization.code})

    def form_valid(self, form):
        org_name = form.cleaned_data["name"]
        self.add_success_notification(org_name)
        return super().form_valid(form)

    def add_success_notification(self, org_name):
        success_message = _("{org_name} succesfully created.").format(org_name=org_name)
        messages.add_message(self.request, messages.SUCCESS, success_message)
