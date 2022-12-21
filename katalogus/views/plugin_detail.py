from logging import getLogger
from django.views import View
from django.http import FileResponse
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.utils.translation import gettext_lazy as _
from django.urls.base import reverse
from katalogus.client import get_katalogus
from katalogus.views import PluginSettingsListView
from katalogus.views.plugin_detail_scan_oois import PluginDetailScanOOI
from katalogus.views.mixins import KATalogusMixin
from organizations.mixins import OrganizationsMixin

logger = getLogger(__name__)


class PluginCoverImgView(OrganizationsMixin, View):
    """Get the cover image of a plugin."""

    def get(self, request, *args, **kwargs):
        return FileResponse(get_katalogus(self.organization.code).get_cover(kwargs["plugin_id"]))


@class_view_decorator(otp_required)
class PluginDetailView(
    KATalogusMixin,
    PluginSettingsListView,
    PluginDetailScanOOI,
):
    """Detail view for a specific plugin. Shows plugin settings and consumable oois for scanning."""

    template_name = "plugin_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = self.plugin
        context["breadcrumbs"] = [
            {
                "url": reverse("katalogus", kwargs={"organization_code": self.organization.code}),
                "text": _("KAT-alogus"),
            },
            {
                "url": reverse(
                    "plugin_detail",
                    kwargs={
                        "organization_code": self.organization.code,
                        "plugin_type": self.plugin["type"],
                        "plugin_id": self.plugin_id,
                    },
                ),
                "text": self.plugin["name"],
            },
        ]
        return context
