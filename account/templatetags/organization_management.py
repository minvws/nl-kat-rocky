from django import template
from django.utils.translation import gettext_lazy as _
from tools.models import Organization, OrganizationMember

register = template.Library()


@register.simple_tag
def get_organizations(user):
    organizations = []
    members = OrganizationMember.objects.filter(user=user)
    if members.exists():
        for member in members:
            organization = Organization.objects.get(name=member.organization)
            organizations.append(organization)
        return organizations
