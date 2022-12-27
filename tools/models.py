import logging
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tagulous.models import TagField

from octopoes.connector.octopoes import OctopoesAPIConnector
from katalogus.client import get_katalogus
from tools.add_ooi_information import get_info, SEPARATOR
from tools.enums import SCAN_LEVEL
from tools.fields import LowerCaseSlugField
from tools.validators import phone_validator

User = get_user_model()

GROUP_ADMIN = "admin"
GROUP_REDTEAM = "redteam"
GROUP_CLIENT = "clients"

logger = logging.getLogger(__name__)


class Organization(models.Model):
    name = models.CharField(max_length=126, unique=True, help_text=_("The name of the organisation"))
    code = LowerCaseSlugField(
        max_length=32,
        unique=True,
        allow_unicode=True,
        help_text=_(
            "A slug containing only lower-case unicode letters, numbers, hyphens or underscores "
            "that will be used in URLs and paths"
        ),
    )
    tags = TagField(force_lowercase=True, protect_all=True, tree=True, blank=True)

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

    def delete(self, *args, **kwargs):
        katalogus_client = get_katalogus(self.code)
        # FIXME: Handle exceptions
        katalogus_client.delete_organization()

        octopoes_client = OctopoesAPIConnector(settings.OCTOPOES_API, client=self.code)
        # FIXME: Handle exceptions
        octopoes_client.delete_node()

        super().delete(*args, **kwargs)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return

        katalogus_client = get_katalogus(instance.code)
        # FIXME: Handle exceptions
        katalogus_client.create_organization(instance.name)

        octopoes_client = OctopoesAPIConnector(settings.OCTOPOES_API, client=instance.code)
        # FIXME: Handle exceptions
        octopoes_client.create_node()


post_save.connect(Organization.post_create, sender=Organization)


class OrganizationMember(models.Model):
    class STATUSES(models.TextChoices):
        ACTIVE = "active", _("active")
        NEW = "new", _("new")
        BLOCKED = "blocked", _("blocked")

    scan_levels = [scan_level.value for scan_level in SCAN_LEVEL]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name="members")
    verified = models.BooleanField(default=False)
    authorized = models.BooleanField(default=False)
    status = models.CharField(choices=STATUSES.choices, max_length=64, default=STATUSES.NEW)
    member_name = models.CharField(max_length=126)
    member_role = models.CharField(max_length=126)
    goal = models.CharField(max_length=256)
    signal_username = models.CharField(
        validators=[phone_validator],
        max_length=126,
        unique=True,
        default=None,
        blank=True,
        null=True,
    )
    onboarded = models.BooleanField(default=False)
    trusted_clearance_level = models.IntegerField(
        default=-1, validators=[MinValueValidator(-1), MaxValueValidator(max(scan_levels))]
    )
    acknowledged_clearance_level = models.IntegerField(
        default=-1, validators=[MinValueValidator(-1), MaxValueValidator(max(scan_levels))]
    )

    def __str__(self):
        return str(self.user)


class Indemnification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)


class OOIInformation(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    last_updated = models.DateTimeField(auto_now=True)
    data = models.JSONField(null=True)
    consult_api = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.data is None:
            self.data = {"description": ""}
        if self.consult_api:
            self.consult_api = False
            self.get_internet_description()
        super(OOIInformation, self).save(*args, **kwargs)

    def clean(self):
        if "description" not in self.data:
            raise ValidationError("Description is missing in data")

    @property
    def type(self):
        return self.id.split(SEPARATOR)[0]

    @property
    def value(self):
        return SEPARATOR.join(self.id.split(SEPARATOR)[1:])

    @property
    def description(self):
        if self.data["description"] == "":
            self.get_internet_description()
        return self.data["description"]

    def get_internet_description(self):
        for key, value in get_info(ooi_type=self.type, natural_key=self.value).items():
            self.data[key] = value
        self.save()

    def __str__(self):
        return self.id


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    boefje_id = models.CharField(max_length=128)
    input_ooi = models.TextField(null=True)
    arguments = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
