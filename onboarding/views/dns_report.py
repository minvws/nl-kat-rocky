from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from onboarding.mixins import OnboardingBreadcrumbsMixin
from onboarding.views.base import BaseReportView
from octopoes.models import OOI
from oois.views import DNSReport
from organizations.mixins import OrganizationsMixin


@class_view_decorator(otp_required)
class DnsReportView(OnboardingBreadcrumbsMixin, BaseReportView, OrganizationsMixin):
    template_name = "dns_report.html"
    report = DNSReport

    def get_ooi(self):
        return self.get_dns_zone_for_url(super().get_ooi(self.organization.code))

    def get_dns_zone_for_url(self, ooi: OOI):
        """
        Path to DNSZone: url > hostnamehttpurl > netloc > fqdn > dns_zone
        """
        if ooi.ooi_type != "URL":
            return ooi

        try:
            web_url = self.tree.store[str(ooi.web_url)]
            netloc = self.tree.store[str(web_url.netloc)]
            fqdn = self.tree.store[str(netloc.fqdn)]
            dns_zone = super().get_ooi(self.organization.code, pk=str(fqdn.dns_zone))
            return dns_zone
        except KeyError:
            messages.add_message(self.request, messages.ERROR, _("No DNS zone found."))
            return ooi
