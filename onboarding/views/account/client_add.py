from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from django.contrib.auth import get_user_model
from onboarding.forms import OnboardingCreateUserClientForm
from onboarding.mixins import RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin

User = get_user_model()


@class_view_decorator(otp_required)
class OnboardingAccountSetupClientView(RegistrationBreadcrumbsMixin, OnboardingAccountCreationMixin):
    """
    View to create a client account
    """

    model = User
    template_name = "account/step_client_add.html"
    form_class = OnboardingCreateUserClientForm
    current_step = 3

    def get_success_url(self, **kwargs):
        return reverse_lazy("crisis_room")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        self.add_success_notification(name)
        return super().form_valid(form)

    def add_success_notification(self, name):
        success_message = _("{name} succesfully created.").format(name=name)
        messages.add_message(self.request, messages.SUCCESS, success_message)
