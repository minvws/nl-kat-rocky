from django.urls import reverse, resolve
from pytest_django.asserts import assertContains

from rocky.views.finding_add import FindingAddView
from tests.conftest import setup_request


def test_findings_add(
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
    url = reverse("finding_add", kwargs=kwargs)
    request = rf.get(url, {"ooi_id": "Network|testnetwork"})
    request.resolver_match = resolve(url)

    setup_request(request, my_user)

    mock_organization_view_octopoes().get.return_value = network

    response = FindingAddView.as_view()(request, **kwargs)

    assert response.status_code == 200
    assertContains(response, "testnetwork")
    assertContains(response, "Add Finding")
    assertContains(response, "Add finding")
