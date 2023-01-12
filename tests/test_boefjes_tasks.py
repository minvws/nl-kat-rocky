from pytest_django.asserts import assertContains
from unittest.mock import call
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from requests import HTTPError
from rocky.views import BoefjesTaskListView


def test_boefjes_tasks(rf, user, organization, mocker, lazy_task_list_empty):
    mock_scheduler_client = mocker.patch("rocky.views.tasks.client")
    mock_scheduler_client.get_lazy_task_list.return_value = lazy_task_list_empty

    request = rf.get(reverse("boefjes_task_list", kwargs={"organization_code": organization.code}))
    request.user = user
    request.organization = organization

    response = BoefjesTaskListView.as_view()(request)

    assert response.status_code == 200

    mock_scheduler_client.get_lazy_task_list.assert_has_calls(
        [
            call(
                scheduler_id="boefje-test",
                object_type="boefje",
                status=None,
                min_created_at=None,
                max_created_at=None,
            )
        ]
    )


def test_tasks_view_simple(rf, user, organization, mocker, lazy_task_list_with_boefje):
    mock_scheduler_client = mocker.patch("rocky.views.tasks.client")
    mock_scheduler_client.get_lazy_task_list.return_value = lazy_task_list_with_boefje

    request = rf.get(reverse("task_list", kwargs={"organization_code": organization.code}))
    request.user = user

    response = BoefjesTaskListView.as_view()(request)

    assertContains(response, "1b20f85f")
    assertContains(response, "Hostname|internet|mispo.es.")

    mock_scheduler_client.get_lazy_task_list.assert_has_calls(
        [
            call(
                scheduler_id="boefje-test",
                object_type="boefje",
                status=None,
                min_created_at=None,
                max_created_at=None,
            )
        ]
    )


def test_tasks_view_error(rf, user, organization, mocker, lazy_task_list_with_boefje):
    mock_scheduler_client = mocker.patch("rocky.views.tasks.client")
    mock_scheduler_client.get_lazy_task_list.return_value = lazy_task_list_with_boefje
    mock_scheduler_client.get_lazy_task_list.side_effect = HTTPError

    request = rf.get(reverse("task_list", kwargs={"organization_code": organization.code}))
    request.user = user
    request.session = "session"
    request._messages = FallbackStorage(request)

    response = BoefjesTaskListView.as_view()(request)

    assertContains(response, "error")
    assertContains(response, "Fetching tasks failed")
