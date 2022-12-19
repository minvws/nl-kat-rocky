from django.urls import path, include
from oois import views

urlpatterns = [
    path("objects/graph/", views.OOIGraphView.as_view(), name="ooi_graph"),
    path("objects/report/", views.OOIReportView.as_view(), name="ooi_report"),
    path("objects/report/pdf/", views.OOIReportPDFView.as_view(), name="ooi_pdf_report"),
    path("objects/summary/", views.OOISummaryView.as_view(), name="ooi_summary"),
    path("objects/tree/", views.OOITreeView.as_view(), name="ooi_tree"),
    path("objects/findings/", views.OOIFindingListView.as_view(), name="ooi_findings"),
    path("objects/", views.OOIListView.as_view(), name="ooi_list"),
    path("objects/add/", views.OOIAddTypeSelectView.as_view(), name="ooi_add_type_select"),
    path(
        "objects/add-related/",
        views.OOIRelatedObjectAddView.as_view(),
        name="ooi_add_related",
    ),
    path("objects/add/<ooi_type>/", views.OOIAddView.as_view(), name="ooi_add"),
    path("objects/edit/", views.OOIEditView.as_view(), name="ooi_edit"),
    path("objects/delete/", views.OOIDeleteView.as_view(), name="ooi_delete"),
    path("objects/detail/", views.OOIDetailView.as_view(), name="ooi_detail"),
    path("objects/export", views.OOIListExportView.as_view(), name="ooi_list_export"),
    path(
        "objects/indemnification/reset/",
        views.ScanProfileResetView.as_view(),
        name="scan_profile_reset",
    ),
    path(
        "objects/scan-profile/",
        views.ScanProfileDetailView.as_view(),
        name="scan_profile_detail",
    ),
    path("scans/", views.ScanListView.as_view(), name="scan_list"),
    path(
        "upload/csv/",
        views.UploadCSV.as_view(),
        name="upload_csv",
    ),
]
