from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from organizations.models import Organization, OrganizationMember
from account.forms import UserAddForm, GroupAddForm
from organizations.models import ORGANIZATION_CODE_LENGTH

User = get_user_model()


class OrganizationMemberAddForm(UserAddForm, forms.ModelForm):
    """
    Form to add a new member
    """

    group = None

    def __init__(self, *args, **kwargs):
        if "organization_name" in kwargs:
            self.organization = self.get_organization_with_name(kwargs.pop("organization_name"))
        elif "organization_id" in kwargs:
            self.organization = self.get_organization_with_id(kwargs.pop("organization_id"))
        return super().__init__(*args, **kwargs)

    def get_organization_with_id(self, id):
        return Organization.objects.get(pk=id)

    def get_organization_with_name(self, organization_name):
        return Organization.objects.get(name=organization_name)

    def set_organization_member(self):
        OrganizationMember.objects.get_or_create(
            user=self.user,
            organization=self.organization,
            verified=True,
            member_name=self.cleaned_data["name"],
        )

    def save(self, **kwargs):
        if self.group:
            selected_group = Group.objects.get(name=self.group)
        else:
            selected_group = Group.objects.get(name=self.cleaned_data["account_type"])
        if self.organization and selected_group:
            self.set_user()
            self.set_organization_member()
            selected_group.user_set.add(self.user)
            self.user.save()


class OrganizationMemberToGroupAddForm(GroupAddForm, OrganizationMemberAddForm):
    class Meta:
        model = User
        fields = ("account_type", "name", "email", "password")


class OrganizationMemberForm(forms.ModelForm):
    class Meta:
        model = OrganizationMember
        fields = ["organization"]


class OrganizationForm(forms.ModelForm):
    """
    Form to create a new organization.
    """

    class Meta:
        model = Organization
        fields = ["name", "code"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": _("The name of the organization."),
                    "autocomplete": "off",
                    "aria-describedby": _("explanation-organization-name"),
                },
            ),
            "code": forms.TextInput(
                attrs={
                    "placeholder": _("A unique code of {code_length} characters.").format(
                        code_length=ORGANIZATION_CODE_LENGTH
                    ),
                    "autocomplete": "off",
                    "aria-describedby": _("explanation-organization-code"),
                },
            ),
        }
        error_messages = {
            "name": {
                "required": _("Organization name is required to proceed."),
                "unique": _("Choose another organization."),
            },
            "code": {
                "required": _("Organization code is required to proceed."),
                "unique": _("Choose another code for your organization."),
            },
        }
