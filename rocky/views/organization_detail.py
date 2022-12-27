from enum import Enum
from typing import Dict, List
from django.urls.base import reverse
from django.views.generic import ListView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from tools.models import Organization
from tools.view_helpers import Breadcrumb, OrganizationBreadcrumbsMixin
from account.mixins import OrganizationsMixin
from tools.models import OrganizationMember


class PageActions(Enum):
    SIGNAL_GROUP_CREATE = "signal_group_create"
    SIGNAL_GROUP_ADD_MEMBER = "signal_group_add_member"
    SIGNAL_GROUP_SEND_TEST_MESSAGE = "signal_group_send_test_message"
    GIVE_CLEARANCE = "give_clearance"


def is_allowed_action_for_organization(action: PageActions, organization: Organization) -> bool:
    return False


def get_allowed_actions(organization) -> Dict[str, bool]:
    return {action.value: is_allowed_action_for_organization(action, organization) for action in PageActions}


@class_view_decorator(otp_required)
class OrganizationDetailView(PermissionRequiredMixin, OrganizationBreadcrumbsMixin, ListView, OrganizationsMixin):
    model = Organization
    template_name = "organizations/organization_detail.html"
    permission_required = "organizations.view_organization"
    context_object_name = "organization"

    def get_members(self):
        return OrganizationMember.objects.filter(organization=self.organization)

    def get_queryset(self):
        """
        List organization that only belongs to user that requests the list.
        """

        object = self.model.objects.get(code=self.organization.code)
        return object

    def build_breadcrumbs(self) -> List[Breadcrumb]:
        breadcrumbs = super().build_breadcrumbs()
        breadcrumbs.append(
            {
                "url": reverse("organization_detail", kwargs={"organization_code": self.organization.code}),
                "text": self.organization.name,
            },
        )

        return breadcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.get_members()
        return context
