from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from octopoes.models.ooi.findings import Finding
from oois.views import BaseOOIListView
from rocky.view_helpers import BreadcrumbsMixin
from organizations.mixins import OrganizationsMixin


class FindingListView(BreadcrumbsMixin, BaseOOIListView):
    template_name = "finding_list.html"
    ooi_types = {Finding}

    def build_breadcrumbs(self):
        return [
            {
                "url": reverse_lazy("finding_list", kwargs={"organization_code": self.organization.code}),
                "text": _("Findings"),
            }
        ]
