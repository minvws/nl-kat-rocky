from pytest_django.asserts import assertContains

from katalogus.views import KATalogusView
from tests.conftest import setup_request


def test_katalogus_plugin_listing(my_user, rf, organization, mocker):
    mocker.patch("katalogus.client.KATalogusClientV1")

    request = setup_request(rf.get("katalogus"), my_user)
    response = KATalogusView.as_view()(request, organization_code=organization.code)

    assertContains(response, "KAT-alogus")
