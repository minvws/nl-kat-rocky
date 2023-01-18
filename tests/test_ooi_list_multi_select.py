from django.urls import reverse, resolve
from rocky.views.ooi_list import OOIListView
from tests.conftest import setup_request
from tools.models import OrganizationMember


def test_ooi_list_delete_multiple(rf, my_user, organization, mock_organization_view_octopoes):
    kwargs = {"organization_code": organization.code}
    url = reverse("ooi_list", kwargs=kwargs)

    request = rf.post(
        url,
        data={
            "ooi": ["Network|internet", "Hostname|internet|scanme.org."],
            "scan-profile": "L0",
            "action": "delete",
        },
    )
    request.resolver_match = resolve(url)
    setup_request(request, my_user)

    my_user.acknowledged_clearance_level = 0
    my_user.save()
    response = OOIListView.as_view()(request, **kwargs)

    assert response.status_code == 200
    assert mock_organization_view_octopoes().list.call_count == 2
    assert mock_organization_view_octopoes().delete.call_count == 2


def test_update_scan_profile_multiple(rf, my_user, organization, mock_organization_view_octopoes):
    kwargs = {"organization_code": organization.code}
    url = reverse("ooi_list", kwargs=kwargs)

    request = rf.post(
        url,
        data={
            "ooi": ["Network|internet", "Hostname|internet|scanme.org."],
            "scan-profile": "L1",
            "action": "update-scan-profile",
        },
    )
    request.resolver_match = resolve(url)
    setup_request(request, my_user)
    response = OOIListView.as_view()(request, **kwargs)

    assert response.status_code == 200
    assert mock_organization_view_octopoes().save_scan_profile.call_count == 2


def test_update_scan_profile_single(rf, my_user, organization, mock_organization_view_octopoes):
    kwargs = {"organization_code": organization.code}
    url = reverse("ooi_list", kwargs=kwargs)

    request = rf.post(
        url,
        data={
            "ooi": ["Hostname|internet|scanme.org."],
            "scan-profile": "L4",
            "action": "update-scan-profile",
        },
    )
    request.resolver_match = resolve(url)
    setup_request(request, my_user)
    response = OOIListView.as_view()(request, **kwargs)

    assert response.status_code == 200
    assert mock_organization_view_octopoes().save_scan_profile.call_count == 1


def test_update_scan_profiles_forbidden_acknowledged(rf, my_user, organization, mock_organization_view_octopoes):
    kwargs = {"organization_code": organization.code}
    url = reverse("ooi_list", kwargs=kwargs)

    request = rf.post(
        url,
        data={
            "ooi": ["Network|internet", "Hostname|internet|scanme.org."],
            "scan-profile": "L1",
            "action": "update-scan-profile",
        },
    )
    request.resolver_match = resolve(url)

    member = OrganizationMember.objects.get(user=my_user)
    member.acknowledged_clearance_level = -1
    member.save()

    setup_request(request, my_user)

    response = OOIListView.as_view()(request, **kwargs)

    assert response.status_code == 403
    assert mock_organization_view_octopoes().save_scan_profile.call_count == 0


def test_update_scan_profiles_forbidden_trusted(rf, my_user, organization, mock_organization_view_octopoes):
    kwargs = {"organization_code": organization.code}
    url = reverse("ooi_list", kwargs=kwargs)

    request = rf.post(
        url,
        data={
            "ooi": ["Network|internet", "Hostname|internet|scanme.org."],
            "scan-profile": "L1",
            "action": "update-scan-profile",
        },
    )
    request.resolver_match = resolve(url)

    member = OrganizationMember.objects.get(user=my_user)
    member.trusted_clearance_level = -1
    member.save()

    setup_request(request, my_user)

    response = OOIListView.as_view()(request, **kwargs)

    assert response.status_code == 403
    assert mock_organization_view_octopoes().save_scan_profile.call_count == 0
