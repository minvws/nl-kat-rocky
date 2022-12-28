from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from octopoes.models.ooi.findings import Finding
from rocky.views import BaseOOIListView
from tools.view_helpers import BreadcrumbsMixin
from account.mixins import OrganizationsMixin


class FindingListView(BreadcrumbsMixin, BaseOOIListView, OrganizationsMixin):
    template_name = "findings/finding_list.html"
    ooi_types = {Finding}

    def build_breadcrumbs(self):
        return [
            {
                "url": reverse_lazy("finding_list", kwargs={"organization_code": self.organization.code}),
                "text": _("Findings"),
            }
        ]
