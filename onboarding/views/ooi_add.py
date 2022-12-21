from typing import Type, List, Dict, Any
from django.contrib import messages
from django.http import Http404
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from octopoes.models import OOI
from octopoes.models.ooi.network import Network
from octopoes.models.types import type_by_name
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import KatIntroductionStepsMixin, RedTeamUserRequiredMixin, OnboardingBreadcrumbsMixin
from onboarding.forms import OnboardingOOIForm
from oois.views import BaseOOIFormView
from oois.ooi_helpers import get_or_create_ooi
from rocky.view_helpers import get_ooi_url, Breadcrumb


@class_view_decorator(otp_required)
class OnboardingSetupScanOOIAddView(
    RedTeamUserRequiredMixin,
    KatIntroductionStepsMixin,
    OnboardingBreadcrumbsMixin,
    BaseOOIFormView,
):
    template_name = "step_ooi_add.html"
    current_step = 3
    form_class = OnboardingOOIForm
    hidden_form_fields = {
        "network": {
            "ooi": Network(name="internet"),
        }
    }

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.ooi_class = self.get_ooi_class()

    def get_hidden_form_fields(self):
        hidden_fields = {}
        for field_name, params in self.hidden_form_fields.items():
            ooi, created = get_or_create_ooi(self.api_connector, params["ooi"])
            hidden_fields[field_name] = ooi.primary_key

            if created:
                messages.success(
                    self.request,
                    _(
                        "KAT added the following required object to your object list to complete your request: {}"
                    ).format(str(ooi)),
                )
        return hidden_fields

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        hidden_fields = self.get_hidden_form_fields()
        kwargs.update({"hidden_fields": hidden_fields, "initial": hidden_fields})

        return kwargs

    def get_ooi_class(self) -> Type[OOI]:
        try:
            return type_by_name(self.kwargs["ooi_type"])
        except KeyError:
            raise Http404("OOI not found")

    def get_success_url(self, ooi: OOI) -> str:
        self.request.session["ooi_id"] = ooi.primary_key
        return get_ooi_url("step_set_clearance_level", ooi.primary_key, organization_code=self.organization.code)

    def build_breadcrumbs(self) -> List[Breadcrumb]:
        return super().build_breadcrumbs() + [
            {
                "url": reverse("ooi_add_type_select"),
                "text": _("Creating an object"),
            },
        ]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["type"] = self.ooi_class.get_ooi_type()
        return context
