from typing import Dict, Type
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from organizations.models import Organization, OrganizationMember, ORGANIZATION_CODE_LENGTH
from oois.models import SCAN_LEVEL
from account.groups import (
    GROUP_ADMIN,
    GROUP_REDTEAM,
    GROUP_CLIENT,
)
from rocky.forms.settings import BLANK_CHOICE
from organizations.forms import OrganizationMemberAddForm
from oois.forms.ooi_form import OOIForm
from octopoes.models import OOI
from octopoes.connector.octopoes import OctopoesAPIConnector

User = get_user_model()


class OnboardingOOIForm(OOIForm):
    """
    hidden_fields - key (field name) value (field value) pair that will rendered as hidden field
    """

    def __init__(
        self, hidden_fields: Dict[str, str], ooi_class: Type[OOI], connector: OctopoesAPIConnector, *args, **kwargs
    ):
        self.hidden_ooi_fields = hidden_fields
        super().__init__(ooi_class, connector, *args, **kwargs)

    def get_fields(self):
        return self.generate_form_fields(self.hidden_ooi_fields)


class ClearanceLevelSelect(forms.Select):
    """Only level 2 is enabled in onboarding flow"""

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get("value") == 2:
            option["attrs"]["disabled"] = "disabled"
        return option


class OnboardingSetClearanceLevelForm(forms.Form):

    level = forms.IntegerField(
        label=_("Clearance level"),
        help_text=_(
            "Boefjes that has a scan level below or equal to the clearance level, is permitted to scan an object."
        ),
        error_messages={
            "level": {
                "required": _("Please select a clearance level to proceed."),
            },
        },
        widget=ClearanceLevelSelect(
            choices=[BLANK_CHOICE] + SCAN_LEVEL.choices,
            attrs={
                "aria-describedby": _("explanation-clearance-level"),
            },
        ),
    )


class OnboardingUserForm(OrganizationMemberAddForm):
    """
    This is the standard form model that is used across all onboarding
    user account creation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_permissions()

    def check_permissions(self):
        if self.group:
            permission = Permission.objects.get(codename="can_set_clearance_level")
            group_object = Group.objects.filter(name=self.group, permissions=permission.id)

        if group_object:
            self.fields["trusted_clearance_level"] = forms.BooleanField(
                label=_("Trusted to set clearance levels on OOI's"),
                widget=forms.CheckboxInput(),
                help_text=_("Give this user permission to set clearance levels on OOI's"),
                required=False,
            )

    class Meta:
        model = OrganizationMember
        fields = ("name", "email", "password")


class OnboardingCreateUserAdminForm(OnboardingUserForm):
    """
    To create an admin account, only superusers and admins
    have this permission.
    """

    group = GROUP_ADMIN


class OnboardingCreateUserRedTeamerForm(OnboardingUserForm):
    """
    Form to create a red teamer user.
    """

    group = GROUP_REDTEAM


class OnboardingCreateUserClientForm(OnboardingUserForm):
    """
    Form to create a client user.
    """

    group = GROUP_CLIENT
