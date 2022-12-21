from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib import messages
from django.views.generic import CreateView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from account.groups import GROUP_ADMIN, GROUP_REDTEAM
from rocky.view_helpers import BreadcrumbsMixin, StepsMixin
from organizations.mixins import OrganizationsMixin


class SuperOrAdminUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        is_admin = self.request.user.groups.filter(name=GROUP_ADMIN).exists()
        return self.request.user.is_superuser or is_admin


class RedTeamUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name=GROUP_REDTEAM).exists()


class RegistrationBreadcrumbsMixin(BreadcrumbsMixin):
    breadcrumbs = [
        {"url": reverse_lazy("step_introduction_registration"), "text": _("KAT Setup")},
    ]


class OnboardingBreadcrumbsMixin(BreadcrumbsMixin):
    breadcrumbs = [
        {"url": reverse_lazy("step_introduction"), "text": _("KAT introduction")},
    ]


class KatIntroductionStepsMixin(StepsMixin):
    steps = [
        {"text": _("1: Introduction"), "url": reverse_lazy("step_introduction")},
        {
            "text": _("2: Choose a report"),
            "url": reverse_lazy("step_choose_report_info"),
        },
        {
            "text": _("3: Setup scan"),
            "url": reverse_lazy("step_setup_scan_ooi_info"),
        },
        {"text": _("4: Open report"), "url": reverse_lazy("step_report")},
    ]


class KatIntroductionAdminStepsMixin(StepsMixin):
    def build_steps(self):
        account_url = ""
        idemnification_url = ""
        if self.organization:
            idemnification_url = reverse_lazy(
                "step_indemnification_setup", kwargs={"organization_code": self.organization.code}
            )
            account_url = reverse_lazy("step_account_setup_intro", kwargs={"organization_code": self.organization.code})

        steps = [
            {
                "text": _("1: Introduction"),
                "url": reverse_lazy("step_introduction_registration"),
            },
            {
                "text": _("2: Organization setup"),
                "url": reverse_lazy("step_organization_setup"),
            },
            {"text": _("3: Account setup"), "url": account_url},
            {"text": _("4: Indemnification"), "url": idemnification_url},
        ]
        return steps


@class_view_decorator(otp_required)
class OnboardingAccountCreationMixin(
    SuperOrAdminUserRequiredMixin, KatIntroductionAdminStepsMixin, OrganizationsMixin, CreateView
):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization_code"] = self.organization.code
        return kwargs
