from django.http import Http404
from django.views import View

from octopoes.connector.octopoes import OctopoesAPIConnector
from rocky.settings import OCTOPOES_API
from tools.models import Organization, OrganizationMember


class OrganizationView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.organization = None
        self.octopoes_api_connector = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        organization_code = kwargs["organization_code"]
        try:
            self.organization = Organization.objects.get(code=organization_code)
        except Organization.DoesNotExist:
            self.organization = None
        self.octopoes_api_connector = OctopoesAPIConnector(OCTOPOES_API, organization_code)

    def dispatch(self, request, *args, **kwargs):

        if self.organization is None:
            raise Http404()

        if (
            not request.user.is_superuser
            and not OrganizationMember.objects.filter(user=self.request.user, organization=self.organization).exists()
        ):
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.organization:
            context["organization"] = self.organization
        return context
