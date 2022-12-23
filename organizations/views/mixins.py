from organizations.models import Organization
from rocky.view_helpers import BreadcrumbsMixin
from django.utils.translation import gettext_lazy as _
from django.urls.base import reverse_lazy, reverse


class OrganizationBreadcrumbsMixin(BreadcrumbsMixin):
    breadcrumbs = [{"url": reverse_lazy("organization_list"), "text": _("Organizations")}]


class OrganizationMemberBreadcrumbsMixin(BreadcrumbsMixin):
    breadcrumb_object: Organization = None

    def set_breadcrumb_object(self, organization: Organization):
        self.breadcrumb_object = organization

    def build_breadcrumbs(self):
        breadcrumbs = [
            {"url": reverse("organization_list"), "text": _("Organizations")},
            {
                "url": reverse("organization_detail", kwargs={"organization_code": self.breadcrumb_object.code}),
                "text": self.breadcrumb_object.name,
            },
            {
                "url": reverse("organization_member_list", kwargs={"organization_code": self.breadcrumb_object.code}),
                "text": _("Members"),
            },
        ]

        return breadcrumbs
