from django.urls import path, include
from django.contrib import admin
from two_factor.urls import urlpatterns as tf_urls
from django.views.generic.base import TemplateView
from rest_framework import routers
from rocky.views import *
from tools.viewsets import OrganizationViewSet
from django.conf.urls.i18n import i18n_patterns

handler404 = "rocky.views.handler404"

router = routers.SimpleRouter()
router.register(r"organization", OrganizationViewSet)

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/v1/", include(router.urls)),
    path("<organization_code>/health/", Health.as_view(), name="health"),
    path("", include(tf_urls)),
    path("", include("account.urls"), name="account"),
]
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("onboarding/", include("onboarding.urls"), name="onboarding"),
    path("crisis-room/", include("crisis_room.urls"), name="crisis_room"),
    path(
        "privacy-statement/",
        PrivacyStatementView.as_view(),
        name="privacy_statement",
    ),
    path(
        "indemnifications/",
        IndemnificationAddView.as_view(),
        name="indemnification_add",
    ),
    path("<organization_code>/findings/", FindingListView.as_view(), name="finding_list"),
    path("<organization_code>/findings/add/", FindingAddView.as_view(), name="finding_add"),
    path("<organization_code>/finding_type/add/", FindingTypeAddView.as_view(), name="finding_type_add"),
    path("<organization_code>/objects/graph/", OOIGraphView.as_view(), name="ooi_graph"),
    path("<organization_code>/objects/report/", OOIReportView.as_view(), name="ooi_report"),
    path("<organization_code>/objects/report/pdf/", OOIReportPDFView.as_view(), name="ooi_pdf_report"),
    path("<organization_code>/objects/summary/", OOISummaryView.as_view(), name="ooi_summary"),
    path("<organization_code>/objects/tree/", OOITreeView.as_view(), name="ooi_tree"),
    path("<organization_code>/objects/findings/", OOIFindingListView.as_view(), name="ooi_findings"),
    path("organizations/", OrganizationListView.as_view(), name="organization_list"),
    path(
        "organizations/add/",
        OrganizationAddView.as_view(),
        name="organization_add",
    ),
    path(
        "organizations/<path:pk>/edit/",
        OrganizationEditView.as_view(),
        name="organization_edit",
    ),
    path(
        "<organization_code>/members/add/",
        OrganizationMemberAddView.as_view(),
        name="organization_member_add",
    ),
    path(
        "<organization_code>/",
        OrganizationDetailView.as_view(),
        name="organization_detail",
    ),
    path(
        "organization_members/<path:pk>/edit/",
        OrganizationMemberEditView.as_view(),
        name="organization_member_edit",
    ),
    path(
        "<organization_code>/health/v1/",
        HealthChecks.as_view(),
        name="health_beautified",
    ),
    path("<organization_code>/objects/", OOIListView.as_view(), name="ooi_list"),
    path("<organization_code>/objects/add/", OOIAddTypeSelectView.as_view(), name="ooi_add_type_select"),
    path(
        "<organization_code>/objects/add-related/",
        OOIRelatedObjectAddView.as_view(),
        name="ooi_add_related",
    ),
    path("<organization_code>/objects/add/<ooi_type>/", OOIAddView.as_view(), name="ooi_add"),
    path("<organization_code>/objects/edit/", OOIEditView.as_view(), name="ooi_edit"),
    path("<organization_code>/objects/delete/", OOIDeleteView.as_view(), name="ooi_delete"),
    path("<organization_code>/objects/detail/", OOIDetailView.as_view(), name="ooi_detail"),
    path("<organization_code>/objects/export", OOIListExportView.as_view(), name="ooi_list_export"),
    path(
        "<organization_code>/objects/indemnification/reset/",
        ScanProfileResetView.as_view(),
        name="scan_profile_reset",
    ),
    path(
        "<organization_code>/objects/scan-profile/",
        ScanProfileDetailView.as_view(),
        name="scan_profile_detail",
    ),
    path("<organization_code>/scans/", ScanListView.as_view(), name="scan_list"),
    path(
        "<organization_code>/upload/csv/",
        UploadCSV.as_view(),
        name="upload_csv",
    ),
    path("<organization_code>/tasks/", BoefjesTaskListView.as_view(), name="task_list"),
    path("<organization_code>/tasks/boefjes", BoefjesTaskListView.as_view(), name="boefjes_task_list"),
    path(
        "<organization_code>/tasks/normalizers",
        NormalizersTaskListView.as_view(),
        name="normalizers_task_list",
    ),
    path(
        "<organization_code>/tasks/<task_id>/download/",
        DownloadTaskDetail.as_view(),
        name="download_task_meta",
    ),
    path("<organization_code>/bytes/<boefje_meta_id>/raw", BytesRawView.as_view(), name="bytes_raw"),
    path("<organization_code>/kat-alogus/", include("katalogus.urls"), name="katalogus"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
)
