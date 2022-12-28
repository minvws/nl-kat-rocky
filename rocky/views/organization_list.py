from django.views.generic import ListView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from tools.models import Organization, OrganizationMember
from tools.view_helpers import OrganizationBreadcrumbsMixin


@class_view_decorator(otp_required)
class OrganizationListView(
    PermissionRequiredMixin,
    OrganizationBreadcrumbsMixin,
    ListView,
):
    model = Organization
    template_name = "organizations/organization_list.html"
    permission_required = "tools.view_organization"

    def get_queryset(self):
        queryset = []
        organizations = self.model.objects.all()
        for organization in organizations:
            total_members = OrganizationMember.objects.filter(organization=organization).count()
            queryset.append({"organization": organization, "total_members": total_members})
        return queryset
