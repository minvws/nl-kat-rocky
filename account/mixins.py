from django.views import View
from tools.models import Organization, OrganizationMember
from django.http import Http404, HttpResponseRedirect


class OrganizationsMixin(View):
    organization = None
    organizationmembers = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return HttpResponseRedirect("login")
        if "organization_code" in kwargs:
            try:
                self.organization = Organization.objects.get(code=kwargs["organization_code"])
                if request.user.is_superuser:
                    self.organizationmembers = OrganizationMember.objects.filter(organization=self.organization)
                else:
                    self.organizationmembers = OrganizationMember.objects.filter(
                        user=self.request.user, organization=self.organization
                    )
                if not self.organizationmembers and not request.user.is_superuser:
                    raise Http404()
            except Organization.DoesNotExist:
                raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.organization:
            context["organization"] = self.organization
        return context
