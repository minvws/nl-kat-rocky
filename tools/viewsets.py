from rest_framework import viewsets

from tools.serializers import OrganizationSerializer, OrganizationSerializerReadOnly
from tools.models import Organization


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    # Unfortunately django-rest-framework doesn't have support for create only
    # fields so we have to change the serializer class depending on the request
    # method.
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method != "POST":
            serializer_class = OrganizationSerializerReadOnly
        return serializer_class
