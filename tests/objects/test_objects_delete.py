from django.urls import reverse, resolve
from pytest_django.asserts import assertContains

from rocky.views.ooi_delete import OOIDeleteView
from tests.conftest import setup_request


def test_ooi_delete(
    rf,
    my_user,
    organization,
    mock_scheduler,
    mock_organization_view_octopoes,
    lazy_task_list_with_boefje,
    mocker,
    network,
):
    mocker.patch("katalogus.utils.get_katalogus")

    kwargs = {"organization_code": organization.code}
    url = reverse("ooi_delete", kwargs=kwargs)
    request = rf.get(url, {"ooi_id": "Network|testnetwork"})
    request.resolver_match = resolve(url)

    setup_request(request, my_user)

    mock_organization_view_octopoes().get.return_value = network

    response = OOIDeleteView.as_view()(request, **kwargs)

    assert response.status_code == 200
    assertContains(response, "testnetwork")
    assertContains(response, "Delete Network")
    assertContains(response, "Are you sure?")
