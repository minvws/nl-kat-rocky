from django.urls import reverse, resolve
from pytest_django.asserts import assertContains

from rocky.views.ooi_edit import OOIEditView
from tests.conftest import setup_request


def test_ooi_edit(
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
    url = reverse("ooi_edit", kwargs=kwargs)
    request = rf.get(url, {"ooi_id": "Network|testnetwork"})
    request.resolver_match = resolve(url)

    setup_request(request, my_user)

    mock_organization_view_octopoes().get.return_value = network

    response = OOIEditView.as_view()(request, **kwargs)

    assert response.status_code == 200
    assertContains(response, "testnetwork")
    assertContains(response, "Save Network")
