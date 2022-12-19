from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth import get_user_model
from onboarding.forms import OnboardingCreateUserClientForm
from onboarding.mixins import RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin
from organizations.models import OrganizationMember


User = get_user_model()


@class_view_decorator(otp_required)
class OnboardingAccountSetupClientView(RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin):
    """
    View to create a client account
    """

    model = User
    template_name = "account/step_6_account_setup_client.html"
    form_class = OnboardingCreateUserClientForm
    succcess_url = reverse_lazy("step_account_setup_client")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # Since this step is optional there is no harm done in setting the
        # "onboarded" bool at setup time.
        member = OrganizationMember.objects.get(user=self.request.user)
        member.onboarded = True
        member.save()

    def get_success_url(self, **kwargs):
        return reverse_lazy("crisis_room")
