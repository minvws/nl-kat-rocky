from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib import messages
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from account.groups import GROUP_ADMIN, GROUP_REDTEAM
from rocky.view_helpers import BreadcrumbsMixin, StepsMixin


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
    steps = [
        {
            "text": _("1: Introduction"),
            "url": reverse_lazy("step_introduction_registration"),
        },
        {
            "text": _("2: Organization setup"),
            "url": reverse_lazy("step_organization_setup"),
        },
        {
            "text": _("3: Indemnification"),
        },
        {
            "text": _("4: Account setup"),
            "url": reverse_lazy("step_account_setup_intro"),
        },
    ]


@class_view_decorator(otp_required)
class OnboardingAccountCreationMixin(SuperOrAdminUserRequiredMixin, KatIntroductionAdminStepsMixin, CreateView):
    current_step = 4

    def dispatch(self, request, *args, **kwargs):
        if "organization_name" not in self.request.session and self.request.user.is_superuser:
            self.add_error_notification()
            return redirect("step_organization_setup")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs["organization_name"] = self.request.session["organization_name"]
        else:
            kwargs["organization_name"] = self.request.active_organization
        return kwargs

    def form_valid(self, form):
        self.add_success_notification()
        return super().form_valid(form)

    def add_success_notification(self):
        success_message = _("User succesfully created.")
        messages.add_message(self.request, messages.SUCCESS, success_message)

    def add_error_notification(self):
        info_message = _(
            "System Administrator: You are redirected to this page, because you have to first setup an organization."
        )
        messages.add_message(self.request, messages.INFO, info_message)
