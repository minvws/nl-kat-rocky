from datetime import datetime
from logging import getLogger

from django.http import FileResponse
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator

from katalogus.client import get_katalogus
from katalogus.views import PluginSettingsListView
from katalogus.views.mixins import KATalogusMixin
from katalogus.views.plugin_detail_scan_oois import PluginDetailScanOOI
from rocky import scheduler

logger = getLogger(__name__)


class PluginCoverImgView(View):
    """Get the cover image of a plugin."""

    def get(self, request, plugin_id: str):
        return FileResponse(get_katalogus(request.active_organization.code).get_cover(plugin_id))


@class_view_decorator(otp_required)
class PluginDetailView(
    KATalogusMixin,
    PluginSettingsListView,
    PluginDetailScanOOI,
):
    """Detail view for a specific plugin. Shows plugin settings and consumable oois for scanning."""

    template_name = "plugin_detail.html"
    scan_history_limit = 10

    def get_scan_history(self) -> scheduler.PaginatedTasksResponse:
        scheduler_id = f"{self.plugin['type']}-{self.request.active_organization.code}"

        filters = [
            {
                "field": f"data__{self.plugin['type']}__id",
                "operator": "eq",
                "value": self.plugin_id,
            }
        ]

        if self.request.GET.get("scan_history_search"):
            filters.append(
                {
                    "field": "data__input_ooi",
                    "operator": "eq",
                    "value": self.request.GET.get("scan_history_search"),
                }
            )

        offset = (int(self.request.GET.get("scan_history_page", 1)) - 1) * self.scan_history_limit

        status = self.request.GET.get("scan_history_status")

        min_created_at = None
        if self.request.GET.get("scan_history_from"):
            min_created_at = datetime.strptime(self.request.GET.get("scan_history_from"), "%Y-%m-%d")

        max_created_at = None
        if self.request.GET.get("scan_history_to"):
            max_created_at = datetime.strptime(self.request.GET.get("scan_history_to"), "%Y-%m-%d")

        scan_history = scheduler.client.list_tasks(
            scheduler_id=scheduler_id,
            limit=self.scan_history_limit,
            offset=offset,
            status=status,
            min_created_at=min_created_at,
            max_created_at=max_created_at,
            filters=filters,
        )

        return scan_history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = self.plugin
        context["breadcrumbs"] = [
            {"url": reverse("katalogus"), "text": _("KAT-alogus")},
            {
                "url": reverse(
                    "plugin_detail", kwargs={"plugin_type": self.plugin["type"], "plugin_id": self.plugin_id}
                ),
                "text": self.plugin["name"],
            },
        ]

        scan_history = self.get_scan_history()
        context["scan_history"] = scan_history
        context["scan_history_pages"] = list(range(1, scan_history.count // self.scan_history_limit + 1))
        context["scan_history_page"] = int(self.request.GET.get("scan_history_page", 1))
        context["scan_history_form_fields"] = [
            "scan_history_from",
            "scan_history_to",
            "scan_history_status",
            "scan_history_search",
            "scan_history_page",
        ]

        return context
