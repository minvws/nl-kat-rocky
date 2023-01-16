from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse, resolve
from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.middleware import OTPMiddleware
from pytest_django.asserts import assertContains

from crisis_room.views import CrisisRoomView
from octopoes.models import Reference
from octopoes.models.ooi.findings import Finding
from octopoes.models.pagination import Paginated
from octopoes.models.types import OOIType


def setup_request(request, user):
    """
    Setup request with middlewares, user, organization and octopoes
    """
    request = SessionMiddleware(lambda r: r)(request)
    request.session[DEVICE_ID_SESSION_KEY] = user.staticdevice_set.get().persistent_id
    request = OTPMiddleware(lambda r: r)(request)
    request = MessageMiddleware(lambda r: r)(request)

    request.user = user

    return request


def test_crisis_room(rf, my_user, organization, mock_crisis_room_octopoes):
    url = reverse("crisis_room")
    request = rf.get(url)
    request.resolver_match = resolve(url)

    setup_request(request, my_user)

    mock_crisis_room_octopoes().list.return_value = Paginated[OOIType](
        count=150, items=[Finding(
            finding_type=Reference.from_str("KATFindingType|KAT-0001"),
            ooi=Reference.from_str("Network|testnetwork"),
            proof="proof",
            description="description",
            reproduce="reproduce",
        )] * 150
    )

    response = CrisisRoomView.as_view()(request)

    assert response.status_code == 200
    assertContains(response, "1")

    assert mock_crisis_room_octopoes().list.call_count == 1
