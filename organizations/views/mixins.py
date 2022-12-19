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
        if self.request.user.has_perm("organizations.can_switch_organization"):
            breadcrumbs = [
                {"url": reverse("organization_list"), "text": _("Organizations")},
                {
                    "url": reverse("organization_detail", kwargs={"pk": self.breadcrumb_object.pk}),
                    "text": self.breadcrumb_object.name,
                },
            ]
        else:
            breadcrumbs = [
                {
                    "url": reverse("crisis_room"),
                    "text": self.breadcrumb_object.name,
                }
            ]

        breadcrumbs.append(
            {
                "url": reverse("organization_member_list", kwargs={"pk": self.breadcrumb_object.pk}),
                "text": _("Members"),
            }
        )

        return breadcrumbs
