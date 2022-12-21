from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from rocky.view_helpers import get_ooi_url

from onboarding.mixins import RedTeamUserRequiredMixin, KatIntroductionStepsMixin, OnboardingBreadcrumbsMixin


@class_view_decorator(otp_required)
class OnboardingReportView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    TemplateView,
):
    template_name = "step_4_report.html"
    current_step = 4

    def get(self, request, *args, **kwargs):
        self.set_current_stepper_url(get_ooi_url("step_report", self.request.GET.get("ooi_id")))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_member_onboarded()
        return redirect(
            get_ooi_url("dns_report", self.request.GET.get("ooi_id"), organization_code=self.organization.code)
        )

    def set_member_onboarded(self):
        member = self.request.user.organizationmember
        member.onboarded = True
        member.save()
