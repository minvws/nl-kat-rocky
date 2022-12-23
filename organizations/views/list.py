from django.views.generic import ListView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from organizations.models import Organization, OrganizationMember
from organizations.views.mixins import OrganizationBreadcrumbsMixin


@class_view_decorator(otp_required)
class OrganizationListView(
    PermissionRequiredMixin,
    OrganizationBreadcrumbsMixin,
    ListView,
):
    model = Organization
    template_name = "organization_list.html"
    permission_required = "organizations.view_organization"
    context_object_name = "organizations"

    def get_queryset(self):
        """
        List all organizations of member.
        """
        organizations = []
        members = OrganizationMember.objects.filter(user=self.request.user)
        if members.exists():
            for member in members:
                organization = Organization.objects.get(name=member.organization)
                organizations.append(organization)
            return organizations
