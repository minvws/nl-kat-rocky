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
    context_object_name = "organizations"

    def get_queryset(self):
        """
        List all organizations of member.
        """
        organizations = []
        self.members = OrganizationMember.objects.filter(user=self.request.user)
        if self.members.exists():
            for member in self.members:
                organization = Organization.objects.get(name=member.organization)
                organizations.append(organization)
            return organizations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.members
        return context
