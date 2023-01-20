from django.urls import reverse, resolve
from pytest_django.asserts import assertContains

from rocky.views.upload_csv import UploadCSV
from tests.conftest import setup_request


def test_csv_upload(rf, my_user, organization,):
    kwargs = {"organization_code": organization.code}
    url = reverse("upload_csv", kwargs=kwargs)
    request = rf.get(url, {"ooi_id": "Network|testnetwork"})
    request.resolver_match = resolve(url)

    setup_request(request, my_user)

    response = UploadCSV.as_view()(request, **kwargs)

    assert response.status_code == 200
    assertContains(response, "Upload CSV")
