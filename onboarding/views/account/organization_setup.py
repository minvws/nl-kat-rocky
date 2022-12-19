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
    View to update the name of a organization
    """

    model = Organization
    template_name = "account/step_organization_setup.html"
    form_class = OrganizationForm
    current_step = 2

    def get_onboarded_organization(self):
        return Organization.objects.first()

    def get(self, request, *args, **kwargs):
        organization = self.get_onboarded_organization()
        if organization:
            return redirect(reverse("step_organization_update", kwargs={"organization_code": organization.code}))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        org_name = form.cleaned_data["name"]
        org_code = form.cleaned_data["code"]
        self.success_url = reverse_lazy("step_indemnification_setup", kwargs={"organization_code": org_code})
        self.add_success_notification(org_name)
        return super().form_valid(form)

    def add_success_notification(self, org_name):
        success_message = _("{org_name} succesfully created.").format(org_name=org_name)
        messages.add_message(self.request, messages.SUCCESS, success_message)

    def add_message(self):
        message = _("Hello, admin. You are already part of an organization. Early step is skipped.")
        messages.add_message(self.request, messages.INFO, message)
