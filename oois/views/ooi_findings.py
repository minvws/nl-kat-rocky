from typing import List, Dict
from katalogus.views.mixins import BoefjeMixin
from oois.views import BaseOOIDetailView
from oois.mixins import OOIBreadcrumbsMixin
from rocky.forms.base import ObservedAtForm
from oois.views import OOIFindingManager
from rocky.view_helpers import Breadcrumb, get_ooi_url
from django.utils.translation import gettext_lazy as _


class OOIFindingListView(OOIFindingManager, BoefjeMixin, BaseOOIDetailView, OOIBreadcrumbsMixin):
    template_name = "ooi_findings.html"
    connector_form_class = ObservedAtForm

    def build_breadcrumbs(self) -> List[Breadcrumb]:
        breadcrumbs = super().build_breadcrumbs()
        breadcrumbs.append(self.get_last_breadcrumb())
        return breadcrumbs

    def get_last_breadcrumb(self):
        return {
            "url": get_ooi_url("ooi_findings", self.ooi.primary_key, organization_code=self.organization.code),
            "text": _("Object findings"),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["findings"] = self.get_finding_details_sorted_by_score_desc()
        context["breadcrumbs"] = self.build_breadcrumbs()
        return context
