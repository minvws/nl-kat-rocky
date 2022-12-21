from django.views import View
from organizations.models import Organization, OrganizationMember
from django.http import Http404, HttpResponseRedirect


class OrganizationsMixin(View):
    organization = None
    organizationmember = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return HttpResponseRedirect("login")
        if "organization_code" in kwargs:
            try:
                self.organization = Organization.objects.get(code=kwargs["organization_code"])
                self.organizationmember = OrganizationMember.objects.filter(
                    user=request.user, organization=self.organization
                )
            except Organization.DoesNotExist:
                raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.organization:
            context["organization"] = self.organization
        return context
