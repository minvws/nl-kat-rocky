import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from oois.models import SCAN_LEVEL
from organizations.fields import LowerCaseSlugField

User = get_user_model()
SCAN_LEVELS = [scan_level.value for scan_level in SCAN_LEVEL]

ORGANIZATION_CODE_LENGTH = 32


class Organization(models.Model):
    name = models.CharField(max_length=126, unique=True, help_text=_("The name of the organization."))
    code = LowerCaseSlugField(
        max_length=ORGANIZATION_CODE_LENGTH,
        unique=True,
        allow_unicode=True,
        help_text=_(
            "A slug containing only lower-case unicode letters, numbers, hyphens or underscores "
            "that will be used in URLs and paths. Insert a unique code for your organization with a maximum length of {code_length} characters."
        ).format(code_length=ORGANIZATION_CODE_LENGTH),
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        permissions = (
            ("can_switch_organization", "Can switch organization"),
            ("can_scan_organization", "Can scan organization"),
            ("can_enable_disable_boefje", "Can enable or disable boefje"),
            ("can_set_clearance_level", "Can set clearance level"),
        )

    def get_absolute_url(self):
        return reverse("organization_detail", args=[self.pk])


class OrganizationMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    onboarded = models.BooleanField(default=False)
    trusted_clearance_level = models.IntegerField(
        default=-1, validators=[MinValueValidator(-1), MaxValueValidator(max(SCAN_LEVELS))]
    )
    acknowledged_clearance_level = models.IntegerField(
        default=-1, validators=[MinValueValidator(-1), MaxValueValidator(max(SCAN_LEVELS))]
    )

    class Meta:
        unique_together = ["user", "organization"]

    def __str__(self):
        return str(self.user)


class Indemnification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    boefje_id = models.CharField(max_length=128)
    input_ooi = models.TextField(null=True)
    arguments = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
