from tagulous.contrib.drf import TagSerializer
from organizations.models import Organization


class OrganizationSerializer(TagSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "code", "tags"]


class OrganizationSerializerReadOnly(TagSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "code", "tags"]
        read_only_fields = ["code"]
