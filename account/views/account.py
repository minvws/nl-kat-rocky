from enum import Enum
from django.contrib import messages
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django_otp.decorators import otp_required
from requests.exceptions import RequestException
from two_factor.views.utils import class_view_decorator
from tools.models import OrganizationMember
from account.mixins import OrganizationsMixin


class PageActions(Enum):
    ACCEPT_CLEARANCE = "accept_clearance"
    WITHDRAW_ACCEPTANCE = "withdraw_acceptance"


@class_view_decorator(otp_required)
class AccountView(OrganizationsMixin, DetailView):
    template_name = "account_detail.html"

    def get_object(self):
        if "pk" not in self.kwargs:
            return self.request.user
        return super().get_object()

    def post(self, request, *args, **kwargs):
        if "action" not in self.request.POST:
            return self.get(request, *args, **kwargs)

        self.object = self.get_object()
        self.handle_page_action(request.POST["action"])

        return redirect(reverse("account_detail", organization_code=self.organization.code))

    def handle_page_action(self, action: str):
        try:
            organizationmember = OrganizationMember.objects.get(user=self.request.user, organization=self.organization)
            if action == PageActions.ACCEPT_CLEARANCE.value:
                organizationmember.acknowledged_clearance_level = organizationmember.trusted_clearance_level
            elif action == PageActions.WITHDRAW_ACCEPTANCE.value:
                organizationmember.acknowledged_clearance_level = 0
            else:
                raise Exception(f"Unhandled allowed action: {action}")
            organizationmember.save()
        except RequestException as exception:
            messages.add_message(self.request, messages.ERROR, f"{action} failed: '{exception}'")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"url": "", "text": "Account details"},
        ]

        return context
