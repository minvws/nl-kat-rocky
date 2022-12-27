from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from tools.view_helpers import StepsMixin


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
