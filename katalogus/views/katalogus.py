from typing import Any, Dict, List
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, FormView
from django.shortcuts import redirect
from django_otp.decorators import otp_required
from django.contrib import messages
from two_factor.views.utils import class_view_decorator
from account.mixins import OrganizationView
from katalogus.client import get_katalogus
from katalogus.forms import KATalogusFilter


@class_view_decorator(otp_required)
class KATalogusView(ListView, OrganizationView, FormView):
    """View of all plugins in KAT-alogus"""

    template_name = "katalogus.html"
    form_class = KATalogusFilter

    def get(self, request, *args, **kwargs):
        katalogus_client = get_katalogus(self.organization.code)
        self.all_plugins = katalogus_client.get_all_plugins()
        self.filter_options = request.GET.get("filter_options", None)
        self.bulk_action = request.GET.get("bulk-action", None)
        return super().get(request, *args, **kwargs)

    def get_all_boefjes(self) -> List[Dict[str, Any]]:
        plugins = [plugin for plugin in self.all_plugins if plugin["type"] == "boefje"]
        return plugins

    def get_all_normalizers(self) -> List[Dict[str, Any]]:
        return [plugin for plugin in self.all_plugins if plugin["type"] == "normalizer"]

    def get_enabled_boefjes(self) -> List[Dict[str, Any]]:
        return [plugin for plugin in self.all_plugins if plugin["type"] == "boefje" and plugin["enabled"]]

    def get_disabled_boefjes(self) -> List[Dict[str, Any]]:
        return [plugin for plugin in self.all_plugins if plugin["type"] == "boefje" and not plugin["enabled"]]

    def get_queryset(self):
        queryset = self.get_all_boefjes()
        if not self.filter_options and not self.bulk_action:
            return queryset
        if self.filter_options:
            queryset = self.filter_queryset(queryset, self.filter_options)
        if self.bulk_action == "enable":
            queryset = self.filter_queryset(queryset, "disabled")  # enable the disabled
        if self.bulk_action == "disable":
            queryset = self.filter_queryset(queryset, "enabled")  # disable the enabled
        return queryset

    def filter_queryset(self, queryset, filter_options) -> List[Dict[str, Any]]:
        filtered_queryset = {
            "a-z": queryset,
            "z-a": list(reversed(queryset)),
            "enabled": self.get_enabled_boefjes(),
            "disabled": self.get_disabled_boefjes(),
            "enabled-disabled": self.get_enabled_boefjes() + self.get_disabled_boefjes(),
            "disabled-enabled": self.get_disabled_boefjes() + self.get_enabled_boefjes(),
        }
        return filtered_queryset[filter_options]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {
                "url": reverse("katalogus", kwargs={"organization_code": self.organization.code}),
                "text": _("KAT-alogus"),
            },
        ]
        context["view"] = self.request.GET.get("view", None)
        context["bulk_action"] = self.request.GET.get("bulk-action")
        context["form_handler_name"] = "select-plugin-form"
        return context


@class_view_decorator(otp_required)
class KATalogusBulkActions(OrganizationView):
    def post(self, request, *args, **kwargs):
        katalogus_client = get_katalogus(self.organization.code)
        selected_plugin_ids = request.POST.getlist("plugin")

        for plugin_id in selected_plugin_ids:
            katalogus_client.enable_boefje(plugin_id)
        messages.add_message(self.request, messages.SUCCESS, _("Plugins successfuly enabled."))
        return redirect(reverse("katalogus", kwargs={"organization_code": self.organization.code}))
