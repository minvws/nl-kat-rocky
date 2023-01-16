import pytest
from django.urls import reverse, resolve
from pytest_django.asserts import assertContains

from katalogus.views.plugin_detail import PluginDetailView
from octopoes.models.pagination import Paginated
from octopoes.models.types import OOIType
from tests.conftest import setup_request


@pytest.fixture()
def mock_katalogus(mocker):
    return mocker.patch("katalogus.views.mixins.get_katalogus")


def test_plugin_detail(
    rf, my_user, organization, mock_katalogus, plugin_details, plugin_schema, mock_organization_view_octopoes, network
):
    kwargs = {"organization_code": organization.code, "plugin_type": "boefje", "plugin_id": "test-plugin"}
    url = reverse("plugin_detail", kwargs=kwargs)
    request = rf.get(url)
    request.resolver_match = resolve(url)

    setup_request(request, my_user)

    mock_organization_view_octopoes().list.return_value = Paginated[OOIType](count=1, items=[network])
    mock_katalogus().get_plugin_details.return_value = plugin_details
    mock_katalogus().get_plugin_schema.return_value = plugin_schema

    response = PluginDetailView.as_view()(request, **kwargs)
    assertContains(response, "TestBoefje")
    assertContains(response, "Meows to the moon")
    assertContains(response, "testnetwork")
