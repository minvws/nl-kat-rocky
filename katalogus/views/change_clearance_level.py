from django.views.generic import TemplateView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from katalogus.views.mixins import BoefjeMixin
from katalogus.views.mixins import KATalogusMixin
from account.mixins import OrganizationsMixin


@class_view_decorator(otp_required)
class ChangeClearanceLevel(BoefjeMixin, KATalogusMixin, OrganizationsMixin, TemplateView):
    template_name = "change_clearance_level.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if "selected_oois" in request.session:
            self.selected_oois = request.session["selected_oois"]
            self.oois = self.get_oois_objects_from_text_oois(self.selected_oois)

    def get(self, request, *args, **kwargs):
        if "selected_oois" not in request.session:
            messages.add_message(self.request, messages.ERROR, _("Session has terminated, please select OOIs again."))
            return redirect(
                reverse(
                    "plugin_detail",
                    kwargs={
                        "organization_code": self.organization.code,
                        "plugin_id": kwargs["plugin_id"],
                        "plugin_type": kwargs["plugin_type"],
                    },
                )
            )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Start scanning oois at plugin detail page."""
        boefje = self.katalogus_client.get_boefje(self.plugin_id)
        self.run_boefje_for_oois(
            boefje=boefje,
            oois=self.oois,
            api_connector=self.get_api_connector(self.organization.code),
        )
        messages.add_message(self.request, messages.SUCCESS, _("Scanning successfully scheduled."))
        del request.session["selected_oois"]  # delete session
        return redirect(reverse("task_list", kwargs={"organization_code": self.organization.code}))

    def get_oois_objects_from_text_oois(self, oois):
        return [self.get_single_ooi(self.organization.code, pk=ooi_id) for ooi_id in oois]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plugin"] = self.plugin
        context["oois"] = self.oois
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
            {
                "url": reverse(
                    "change_clearance_level",
                    kwargs={
                        "organization_code": self.organization.code,
                        "plugin_type": self.plugin["type"],
                        "plugin_id": self.plugin_id,
                        "scan_level": self.plugin["scan_level"],
                    },
                ),
                "text": _("Change clearance level"),
            },
        ]
        return context
