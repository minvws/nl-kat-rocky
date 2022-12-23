from django.urls import path
from organizations import views

urlpatterns = [
    path("", views.OrganizationListView.as_view(), name="organization_list"),
    path(
        "add/",
        views.OrganizationAddView.as_view(),
        name="organization_add",
    ),
    path(
        "<path:pk>/edit/",
        views.OrganizationEditView.as_view(),
        name="organization_edit",
    ),
    path(
        "<organization_code>/members/add/",
        views.OrganizationMemberAddView.as_view(),
        name="organization_member_add",
    ),
    path(
        "<path:pk>/members/",
        views.OrganizationMemberListView.as_view(),
        name="organization_member_list",
    ),
    path(
        "<organization_code>/",
        views.OrganizationDetailView.as_view(),
        name="organization_detail",
    ),
    path(
        "organization_members/<path:pk>/edit/",
        views.OrganizationMemberEditView.as_view(),
        name="organization_member_edit",
    ),
    path(
        "<organization_code>/indemnifications/",
        views.IndemnificationAddView.as_view(),
        name="indemnification_add",
    ),
]
