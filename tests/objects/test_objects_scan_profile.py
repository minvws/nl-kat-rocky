from pytest_django.asserts import assertContains, assertNotContains

from octopoes.models.tree import ReferenceTree
from rocky.views.scan_profile import ScanProfileDetailView
from tests.conftest import setup_request
from tools.models import OrganizationMember


TREE_DATA = {
    "root": {
        "reference": "Finding|Network|testnetwork|KAT-000",
        "children": {"ooi": [{"reference": "Network|testnetwork", "children": {}}]},
    },
    "store": {
        "Network|testnetwork": {
            "object_type": "Network",
            "primary_key": "Network|testnetwork",
            "name": "testnetwork",
            "scan_profile": {
                "scan_profile_type": "declared",
                "reference": "Network|testnetwork",
                "level": 1,
            },
        },
        "Finding|Network|testnetwork|KAT-000": {
            "object_type": "Finding",
            "primary_key": "Finding|Network|testnetwork|KAT-000",
            "ooi": "Network|testnetwork",
            "finding_type": "KATFindingType|KAT-000",
            "scan_profile": {
                "scan_profile_type": "declared",
                "reference": "Finding|Network|testnetwork|KAT-000",
                "level": 1,
            },
        },
    },
}


def test_scan_profile(rf, my_user, organization, mock_scheduler, mock_organization_view_octopoes, mocker):
    mocker.patch("katalogus.utils.get_katalogus")
    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.parse_obj(TREE_DATA)

    request = setup_request(rf.get("scan_profile_detail", {"ooi_id": "Network|testnetwork"}), my_user)
    response = ScanProfileDetailView.as_view()(request, organization_code=organization.code)

    assert response.status_code == 200
    assert mock_organization_view_octopoes().get_tree.call_count == 2

    assertContains(response, "Set clearance level")


def test_scan_profile_no_permissions_acknowledged(
    rf, my_user, organization, mock_scheduler, mock_organization_view_octopoes, mocker
):
    mocker.patch("katalogus.utils.get_katalogus")
    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.parse_obj(TREE_DATA)

    member = OrganizationMember.objects.get(user=my_user)
    member.acknowledged_clearance_level = -1
    member.save()

    request = setup_request(rf.get("scan_profile_detail", {"ooi_id": "Network|testnetwork"}), my_user)
    response = ScanProfileDetailView.as_view()(request, organization_code=organization.code)

    assert response.status_code == 200
    assert mock_organization_view_octopoes().get_tree.call_count == 2

    assertNotContains(response, "Set clearance level")


def test_scan_profile_no_permissions_trusted(
    rf, my_user, organization, mock_scheduler, mock_organization_view_octopoes, mocker
):
    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.parse_obj(TREE_DATA)
    mocker.patch("katalogus.utils.get_katalogus")

    member = OrganizationMember.objects.get(user=my_user)
    member.trusted_clearance_level = -1
    member.save()

    request = setup_request(rf.get("scan_profile_detail", {"ooi_id": "Network|testnetwork"}), my_user)
    response = ScanProfileDetailView.as_view()(request, organization_code=organization.code)

    assert response.status_code == 200
    assert mock_organization_view_octopoes().get_tree.call_count == 2

    assertNotContains(response, "Set clearance level")