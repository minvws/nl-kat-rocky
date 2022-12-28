from datetime import datetime, timezone
import csv
import io
from typing import Dict
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _
from django.urls.base import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from pydantic import ValidationError
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from octopoes.api.models import Declaration
from octopoes.models.ooi.dns.zone import Hostname
from octopoes.models.ooi.web import URL
from octopoes.models.ooi.network import Network, IPAddressV4, IPAddressV6
from octopoes.connector.octopoes import OctopoesAPIConnector
from rocky.settings import OCTOPOES_API
from tools.forms.upload_csv import (
    UploadCSVForm,
    CSV_ERRORS,
)

CSV_CRITERIAS = [
    _("Add column titles. Followed by each object on a new line."),
    _(
        "For URL object type, a column 'raw' with URL values is required, starting with http:// or https://, optionally a second column 'network' is supported "
    ),
    _(
        "For Hostname object type, a column with 'name' values is required, optionally a second column 'network' is supported "
    ),
    _(
        "For IPAddressV4 and IPAddressV6 object types, a column of 'address' is required, optionally a second column 'network' is supported "
    ),
]


@class_view_decorator(otp_required)
class UploadCSV(PermissionRequiredMixin, FormView):
    template_name = "upload_csv.html"
    form_class = UploadCSVForm
    permission_required = "tools.can_scan_organization"
    success_url = reverse_lazy("ooi_list")
    reference_cache = {"network": {"internet": Network(name="internet")}}
    ooi_types = {
        "hostname": {"type": Hostname},
        "url": {"type": URL},
        "network": {"type": Network, "defaultvalue": "internet", "createargument": "name"},
        "ipaddressv4": {"type": IPAddressV4},
        "ipaddressv6": {"type": IPAddressV6},
    }
    skip_properties = ("object_type", "scan_profile", "primary_key")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.organization_code = request.user.organizationmember.organization.code
        if not self.organization_code:
            self.add_error_notification(CSV_ERRORS["no_org"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"url": reverse("ooi_list"), "text": _("Objects")},
            {"url": reverse("upload_csv"), "text": _("Upload CSV")},
        ]
        context["criterias"] = CSV_CRITERIAS
        return context

    def get_or_create_reference(self, ooi_type_name: str, primary_key: str):
        if ooi_type_name not in self.cache:
            self.cache[ooi_type_name] = {}
        if self.cache[ooi_type_name][primary_key]:
            return self.cache[ooi_type_name][primary_key]
        ooi_type = self.ooi_types[ooi_type_name]["type"]
        createarguments = {self.ooi_types[ooi_type_name]["createargument"]: primary_key}
        referenced_ooi = ooi_type(**createarguments)
        self.cache[ooi_type_name][primary_key] = referenced_ooi
        return referenced_ooi

    def get_ooi_from_csv(self, ooi_type_name: str, values: Dict[str, str]):
        ooi_type = self.ooi_types[ooi_type_name].lower()
        ooi_fields = (
            (field, URL.__fields__[field].type_ == Reference, URL.__fields__[field].required)
            for field in URL.__fields__
            if field not in self.skip_properties
        )
        ooi_dict = {}
        for fieldname, reference, required in ooi_fields:
            if reference:
                try:
                    referenced_ooi = self.get_or_create_reference(
                        values.get(fieldname, self.ooi_types[ooi_type_name]["defaultvalue"])
                    )
                    self._save_ooi(ooi=referenced_ooi, organization=self.organization_code)
                    ooi_dict[fieldname] = referenced_ooi.reference
                except IndexError:
                    if required:
                        raise IndexError(
                            "Required referenced primary-key field '%s' not set and no default present for Type '%s'."
                            % (fieldname, ooi_type_name)
                        )
                    else:
                        ooi_dict[fieldname] = None
            else:
                ooi_dict[fieldname] = values[fieldname]
        return ooi_type(**ooi_dict)

    def _save_ooi(self, ooi, organization) -> None:
        connector = OctopoesAPIConnector(OCTOPOES_API, organization)
        connector.save_declaration(Declaration(ooi=ooi, valid_time=datetime.now(timezone.utc)))

    def form_valid(self, form):
        if not self.proccess_csv(form):
            return redirect("upload_csv")
        return super().form_valid(form)

    def add_error_notification(self, error_message):
        messages.add_message(self.request, messages.ERROR, error_message)
        return False

    def add_success_notification(self, success_message):
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return True

    def proccess_csv(self, form):
        object_type = form.cleaned_data["object_type"]
        csv_file = form.cleaned_data["csv_file"]
        csv_data = io.StringIO(csv_file.read().decode("UTF-8"))
        rows_with_error = []
        try:
            for rownumber, row in enumerate(csv.DictReader(csv_data, delimiter=",", quotechar='"')):
                if not row:
                    continue  # skip empty lines
                try:
                    ooi = self.get_ooi_from_csv(object_type, row)
                    self._save_ooi(ooi=ooi, organization=self.organization_code)
                except ValidationError:
                    rows_with_error.append(rownumber + 1)
            if rows_with_error:
                message = _("Object(s) could not be created for line number(s): ") + ", ".join(
                    map(str, rows_with_error)
                )
                return self.add_error_notification(message)
            self.add_success_notification(_("Object(s) successfully added."))
        except (csv.Error, IndexError):
            return self.add_error_notification(CSV_ERRORS["csv_error"])
