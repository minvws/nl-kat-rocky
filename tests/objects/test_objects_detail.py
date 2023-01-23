from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from pytest_django.asserts import assertContains

from octopoes.models.tree import ReferenceTree
from rocky.views.ooi_detail import OOIDetailView
from tests.conftest import setup_request
from tools.models import Indemnification

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
        },
        "Finding|Network|testnetwork|KAT-000": {
            "object_type": "Finding",
            "primary_key": "Finding|Network|testnetwork|KAT-000",
            "ooi": "Network|testnetwork",
            "finding_type": "KATFindingType|KAT-000",
        },
    },
}


def test_ooi_detail(
    rf, my_user, organization, mock_scheduler, mock_organization_view_octopoes, lazy_task_list_with_boefje, mocker
):
    mocker.patch("katalogus.utils.get_katalogus")

    request = setup_request(rf.get("ooi_detail", {"ooi_id": "Network|testnetwork"}), my_user)

    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.parse_obj(TREE_DATA)
    mock_scheduler.get_lazy_task_list.return_value = lazy_task_list_with_boefje

    response = OOIDetailView.as_view()(request, organization_code=organization.code)

    assert response.status_code == 200
    assert mock_organization_view_octopoes().get_tree.call_count == 2
    assertContains(response, "TestBoefje")
    assertContains(response, "test-boefje")


def test_ooi_detail_start_scan(
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

    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.parse_obj(TREE_DATA)
    mock_organization_view_octopoes().get.return_value = network

    # Passing query params in POST requests is not well-supported for RequestFactory it seems, hence the absolute path
    query_string = urlencode({"ooi_id": network.reference}, doseq=True)

    request = setup_request(
        rf.post(
            f"/en/{organization.code}/objects/details/?{query_string}",
            data={
                "boefje_id": "nmap",
                "action": "start_scan",
            },
        ),
        my_user,
    )
    response = OOIDetailView.as_view()(request, organization_code=organization.code)

    assert mock_organization_view_octopoes().get_tree.call_count == 1
    assert isinstance(response, HttpResponseRedirect)
    assert response.status_code == 302
    assert response.url == f"/en/{organization.code}/tasks/"


def test_ooi_detail_start_scan_no_indemnification(
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

    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.parse_obj(TREE_DATA)
    mock_organization_view_octopoes().get.return_value = network

    Indemnification.objects.get(user=my_user).delete()

    # Passing query params in POST requests is not well-supported for RequestFactory it seems, hence the absolute path
    query_string = urlencode({"ooi_id": network.reference}, doseq=True)
    request = setup_request(
        rf.post(
            f"/en/{organization.code}/objects/details/?{query_string}",
            data={
                "boefje_id": "nmap",
                "action": "start_scan",
            },
        ),
        my_user,
    )
    response = OOIDetailView.as_view()(request, organization_code=organization.code)

    assert mock_organization_view_octopoes().get_tree.call_count == 2
    assertContains(response, "Object details", status_code=403)
    assertContains(response, "Indemnification not present", status_code=403)


def test_ooi_detail_start_scan_no_action(
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

    mock_organization_view_octopoes().get_tree.return_value = ReferenceTree.parse_obj(TREE_DATA)
    mock_organization_view_octopoes().get.return_value = network

    # Passing query params in POST requests is not well-supported for RequestFactory it seems, hence the absolute path
    query_string = urlencode({"ooi_id": network.reference}, doseq=True)
    request = setup_request(
        rf.post(
            f"/en/{organization.code}/objects/details/?{query_string}",
            data={
                "boefje_id": "nmap",
            },
        ),
        my_user,
    )
    response = OOIDetailView.as_view()(request, organization_code=organization.code)

    assert mock_organization_view_octopoes().get_tree.call_count == 2
    assertContains(response, "Object details", status_code=404)
