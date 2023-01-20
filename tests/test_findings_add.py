from django.urls import reverse, resolve
from pytest_django.asserts import assertContains

from rocky.views.finding_add import FindingAddView
from tests.conftest import setup_request


def test_findings_add(rf, my_user, organization, mock_organization_view_octopoes):
    kwargs = {"organization_code": organization.code}
    url = reverse("finding_add", kwargs=kwargs)
    request = rf.get(url)
    request.resolver_match = resolve(url)

    setup_request(request, my_user)

    response = FindingAddView.as_view()(request, **kwargs)

    assert response.status_code == 200
    assertContains(response, "Add Finding")
    assertContains(response, "Add finding")
