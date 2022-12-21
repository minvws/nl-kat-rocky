from django import template
from django.utils.translation import gettext_lazy as _
from organizations.models import Organization, OrganizationMember

register = template.Library()


@register.simple_tag
def get_organization_code(user):
    member = OrganizationMember.objects.filter(user=user)
    if member.exists():
        organization = Organization.objects.get(name=member.first().organization)
        return organization.code
