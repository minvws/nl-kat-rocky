from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from oois.add_ooi_information import get_info, SEPARATOR


class SCAN_LEVEL(models.IntegerChoices):
    L0 = 0, "L0"
    L1 = 1, "L1"
    L2 = 2, "L2"
    L3 = 3, "L3"
    L4 = 4, "L4"


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
